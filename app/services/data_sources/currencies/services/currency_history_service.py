"""
货币报价历史数据服务
"""
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.currency_history_provider import CurrencyHistoryProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class CurrencyHistoryService:
    """货币报价历史数据服务"""
    
    # 唯一标识字段
    UNIQUE_KEYS = ["currency", "base", "date"]
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["currency_history"]
        self.provider = CurrencyHistoryProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        
        latest = await self.collection.find_one(sort=[("date", -1)])
        oldest = await self.collection.find_one(sort=[("date", 1)])
        
        # 统计不同基础货币的数量
        pipeline = [
            {"$group": {"_id": "$base", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        base_stats = await self.collection.aggregate(pipeline).to_list(length=100)
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("date") if latest else None,
            "oldest_date": oldest.get("date") if oldest else None,
            "base_stats": base_stats,
        }
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("date", -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（指定日期的历史汇率）
        
        Args:
            base: 基础货币
            date: 日期 YYYY-MM-DD
            symbols: 目标货币
            api_key: API密钥
        """
        try:
            date = kwargs.get("date")
            if not date:
                return {"success": False, "message": "缺少必须参数: date", "inserted": 0}
            
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            records = df.to_dict('records')
            
            # 批量 upsert
            ops = []
            for record in records:
                currency = str(record.get("currency", "")).strip()
                base = str(record.get("base", "")).strip()
                date_val = record.get("date")
                
                if not currency or not base or not date_val:
                    continue
                
                date_str = date_val.isoformat() if hasattr(date_val, 'isoformat') else str(date_val)
                record["date"] = date_str
                record["updated_at"] = datetime.now().isoformat()
                
                ops.append(UpdateOne(
                    {"currency": currency, "base": base, "date": date_str},
                    {"$set": record, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                    upsert=True
                ))
            
            if ops:
                result = await self.collection.bulk_write(ops, ordered=False)
                count = (result.upserted_count or 0) + (result.modified_count or 0)
                return {
                    "success": True,
                    "message": f"Data updated successfully",
                    "inserted": count,
                }
            
            return {
                "success": True,
                "message": "No operations performed",
                "inserted": 0,
            }
            
        except Exception as e:
            logger.error(f"Error updating single data: {e}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新历史数据
        
        Args:
            task_id: 任务ID
            base: 基础货币，默认 USD
            date: 日期 YYYY-MM-DD (必须)
            api_key: API密钥
            max_codes: 最大货币数量
            batch_size: 每批数量
        """
        task_manager = get_task_manager() if task_id else None
        api_key = kwargs.get("api_key")
        date = kwargs.get("date")
        base = kwargs.get("base", "USD")
        max_codes = int(kwargs.get("max_codes", 100))
        batch_size = int(kwargs.get("batch_size", 20))
        
        if not api_key:
            if task_manager:
                task_manager.fail_task(task_id, "缺少必须参数: api_key")
            return {"success": False, "message": "缺少必须参数: api_key"}
        
        if not date:
            if task_manager:
                task_manager.fail_task(task_id, "缺少必须参数: date")
            return {"success": False, "message": "缺少必须参数: date"}
        
        try:
            # 从 currency_currencies 获取货币代码列表
            codes_collection = self.db.get_collection("currency_currencies")
            cursor = codes_collection.find({}, {"code": 1})
            codes = []
            async for doc in cursor:
                code_val = doc.get("code")
                if code_val:
                    codes.append(str(code_val).strip())
                if len(codes) >= max_codes:
                    break
            
            if not codes:
                if task_manager:
                    task_manager.fail_task(task_id, "No currency codes found in currency_currencies collection")
                return {"success": False, "message": "No currency codes found"}
            
            total_saved = 0
            total_batches = len(range(0, len(codes), batch_size))
            
            for batch_idx, i in enumerate(range(0, len(codes), batch_size)):
                if task_manager:
                    progress = int((batch_idx / total_batches) * 100)
                    task_manager.update_progress(task_id, progress, 100, f"正在处理第 {batch_idx + 1}/{total_batches} 批...")
                
                batch_codes = sorted(set(codes[i:i + batch_size]))
                symbols = ",".join(batch_codes)
                
                try:
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: self.provider.fetch_data(
                            base=base, date=date, symbols=symbols, api_key=api_key
                        )
                    )
                    
                    if df is not None and not df.empty:
                        records = df.to_dict('records')
                        ops = []
                        
                        for record in records:
                            currency = str(record.get("currency", "")).strip()
                            base_val = str(record.get("base", "")).strip()
                            date_val = record.get("date")
                            
                            if not currency or not base_val or not date_val:
                                continue
                            
                            date_str = date_val.isoformat() if hasattr(date_val, 'isoformat') else str(date_val)
                            record["date"] = date_str
                            record["updated_at"] = datetime.now().isoformat()
                            
                            ops.append(UpdateOne(
                                {"currency": currency, "base": base_val, "date": date_str},
                                {"$set": record, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                                upsert=True
                            ))
                        
                        if ops:
                            result = await self.collection.bulk_write(ops, ordered=False)
                            count = (result.upserted_count or 0) + (result.modified_count or 0)
                            total_saved += count
                            
                except Exception as e:
                    logger.error(f"Error in batch {batch_idx + 1}: {e}")
                    continue
            
            message = f"批量同步完成，共保存 {total_saved} 条数据"
            
            if task_manager:
                task_manager.complete_task(
                    task_id,
                    result={"saved": total_saved, "codes": len(codes), "batches": total_batches},
                    message=message
                )
            
            return {
                "success": True,
                "message": message,
                "inserted": total_saved,
            }
            
        except Exception as e:
            logger.error(f"Batch update failed: {e}")
            if task_manager:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }

    async def clear_data(self) -> Dict[str, Any]:
        """清空集合数据"""
        result = await self.collection.delete_many({})
        return {
            "success": True,
            "message": f"Cleared {result.deleted_count} records",
            "deleted": result.deleted_count,
        }
