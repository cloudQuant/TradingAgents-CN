"""
货币基础信息数据服务
"""
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.currency_currencies_provider import CurrencyCurrenciesProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class CurrencyCurrenciesService:
    """货币基础信息数据服务"""
    
    # 唯一标识字段
    UNIQUE_KEYS = ["id"]
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["currency_currencies"]
        self.provider = CurrencyCurrenciesProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        # 按货币类型统计
        pipeline = [
            {"$group": {"_id": "$货币类型", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        type_stats = await self.collection.aggregate(pipeline).to_list(length=10)
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
            "type_stats": type_stats,
        }
    
    async def get_data(self, skip: int = 0, limit: int = 100, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("id", 1)
        data = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {"data": data, "total": total, "skip": skip, "limit": limit}

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """更新单条数据（指定货币类型的基础信息）"""
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {"success": True, "message": "No data available", "inserted": 0}
            
            records = df.to_dict('records')
            ops = []
            
            for record in records:
                id_val = record.get("id")
                if not id_val:
                    continue
                
                record["updated_at"] = datetime.now().isoformat()
                record = {k: v for k, v in record.items() if v is not None}
                
                ops.append(UpdateOne(
                    {"id": id_val},
                    {"$set": record, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                    upsert=True
                ))
            
            if ops:
                result = await self.collection.bulk_write(ops, ordered=False)
                count = (result.upserted_count or 0) + (result.modified_count or 0)
                return {"success": True, "message": "Data updated successfully", "inserted": count}
            
            return {"success": True, "message": "No operations performed", "inserted": 0}
            
        except Exception as e:
            logger.error(f"Error updating single data: {e}")
            return {"success": False, "message": str(e), "inserted": 0}

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新货币基础信息（fiat 和 crypto 两种类型）"""
        task_manager = get_task_manager() if task_id else None
        api_key = kwargs.get("api_key")
        
        if not api_key:
            msg = "缺少必须参数: api_key"
            if task_manager:
                task_manager.fail_task(task_id, msg)
            return {"success": False, "message": msg}
        
        c_types = ["fiat", "crypto"]
        total_saved = 0
        success_count = 0
        
        try:
            for idx, c_type in enumerate(c_types):
                if task_manager:
                    progress = int((idx / len(c_types)) * 100)
                    task_manager.update_progress(task_id, progress, 100, f"正在同步 {c_type} 货币数据...")
                
                try:
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda ct=c_type: self.provider.fetch_data(c_type=ct, api_key=api_key)
                    )
                    
                    if df is not None and not df.empty:
                        records = df.to_dict('records')
                        ops = []
                        
                        for record in records:
                            id_val = record.get("id")
                            if not id_val:
                                continue
                            record["updated_at"] = datetime.now().isoformat()
                            record = {k: v for k, v in record.items() if v is not None}
                            ops.append(UpdateOne(
                                {"id": id_val},
                                {"$set": record, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                                upsert=True
                            ))
                        
                        if ops:
                            result = await self.collection.bulk_write(ops, ordered=False)
                            count = (result.upserted_count or 0) + (result.modified_count or 0)
                            total_saved += count
                            success_count += 1
                            logger.info(f"Saved {count} records for c_type={c_type}")
                            
                except Exception as e:
                    logger.error(f"Error syncing c_type={c_type}: {e}")
            
            message = f"批量同步完成: 成功 {success_count}/{len(c_types)}, 共保存 {total_saved} 条数据"
            
            if task_manager:
                task_manager.complete_task(
                    task_id,
                    result={"saved": total_saved, "success": success_count},
                    message=message
                )
            
            return {"success": True, "message": message, "inserted": total_saved}
            
        except Exception as e:
            logger.error(f"Batch update failed: {e}")
            if task_manager:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}

    async def clear_data(self) -> Dict[str, Any]:
        """清空集合数据"""
        result = await self.collection.delete_many({})
        return {"success": True, "message": f"Cleared {result.deleted_count} records", "deleted": result.deleted_count}
