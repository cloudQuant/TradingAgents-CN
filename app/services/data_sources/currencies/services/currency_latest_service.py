"""
货币报价最新数据服务
"""
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.currency_latest_provider import CurrencyLatestProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class CurrencyLatestService:
    """货币报价最新数据服务"""
    
    # 唯一标识字段
    UNIQUE_KEYS = ["currency", "base", "date"]
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["currency_latest"]
        self.provider = CurrencyLatestProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        # 统计不同基础货币的数量
        pipeline = [
            {"$group": {"_id": "$base", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        base_stats = await self.collection.aggregate(pipeline).to_list(length=100)
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
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
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("scraped_at", -1)
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
        更新单条数据（指定基础货币的最新汇率）
        
        Args:
            base: 基础货币
            symbols: 目标货币
            api_key: API密钥
        """
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {"success": True, "message": "No data available", "inserted": 0}
            
            # 使用 ControlMongodb 进行数据去重
            control_db = ControlMongodb(self.collection, self.UNIQUE_KEYS)
            result = await control_db.save_dataframe_to_collection(
                df,
                extra_fields={"数据源": "akshare", "接口名称": "currency_latest"}
            )
            
            return {
                "success": True,
                "message": "Data updated successfully",
                "inserted": result.get("upserted", 0) + result.get("modified", 0),
                "result": result
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
        批量更新数据（USD 和 CNY 两个基础货币）
        
        Args:
            task_id: 任务ID，用于更新进度
            api_key: API密钥
            concurrency: 并发数，默认2
        """
        task_manager = get_task_manager() if task_id else None
        api_key = kwargs.get("api_key")
        
        if not api_key:
            if task_manager:
                task_manager.fail_task(task_id, "缺少必须参数: api_key")
            return {"success": False, "message": "缺少必须参数: api_key"}
        
        # 固定只同步 USD 和 CNY
        bases = ["USD", "CNY"]
        total_saved = 0
        success_count = 0
        failed_count = 0
        
        try:
            for idx, base in enumerate(bases):
                if task_manager:
                    progress = int((idx / len(bases)) * 100)
                    task_manager.update_progress(task_id, progress, 100, f"正在同步 {base} 汇率数据...")
                
                try:
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda b=base: self.provider.fetch_data(base=b, symbols="", api_key=api_key)
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
                            success_count += 1
                            logger.info(f"Saved {count} records for base={base}")
                            
                except Exception as e:
                    logger.error(f"Error syncing base={base}: {e}")
                    failed_count += 1
                    continue
            
            message = f"批量同步完成: 成功 {success_count}/{len(bases)}, 共保存 {total_saved} 条数据"
            
            if task_manager:
                task_manager.complete_task(
                    task_id,
                    result={"saved": total_saved, "success": success_count, "failed": failed_count},
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
