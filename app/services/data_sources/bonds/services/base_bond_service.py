"""
债券服务基类
提供通用的服务模板
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class BaseBondService:
    """债券服务基类"""
    
    def __init__(self, db: AsyncIOMotorClient, collection_name: str, provider, unique_keys: List[str] = None):
        self.db = db
        self.collection = db[collection_name]
        self.collection_name = collection_name
        self.provider = provider
        self.unique_keys = unique_keys or []
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        latest = await self.collection.find_one(sort=[("更新时间", -1)])
        return {
            "total_count": total_count,
            "last_updated": latest.get("更新时间") if latest else None,
        }
    
    async def get_data(self, skip: int = 0, limit: int = 100, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("更新时间", -1)
        data = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        for item in data:
            item["_id"] = str(item["_id"])
        return {"data": data, "total": total, "skip": skip, "limit": limit}
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空数据"""
        result = await self.collection.delete_many({})
        return {"success": True, "deleted": result.deleted_count}
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """单条更新（子类可覆盖）"""
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df is None or df.empty:
                return {"success": True, "message": "No data available", "inserted": 0}
            
            if self.unique_keys:
                control_db = ControlMongodb(self.collection, self.unique_keys)
                result = await control_db.save_dataframe_to_collection(df)
            else:
                # 无唯一键，直接插入
                records = df.to_dict(orient="records")
                if records:
                    await self.collection.insert_many(records)
                result = {"success": True, "inserted": len(records), "updated": 0}
            
            return {
                "success": result.get("success", True),
                "message": result.get("message", ""),
                "inserted": result.get("inserted", 0) + result.get("updated", 0)
            }
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}")
            return {"success": False, "message": str(e), "inserted": 0}

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新（子类可覆盖）"""
        try:
            task_manager = get_task_manager() if task_id else None
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"正在获取 {self.collection_name} 数据...")
            
            df = await asyncio.get_event_loop().run_in_executor(None, lambda: self.provider.fetch_data(**kwargs))
            
            if df is None or df.empty:
                if task_manager and task_id:
                    task_manager.fail_task(task_id, "未获取到数据")
                return {"success": False, "message": "未获取到数据", "inserted": 0}
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
            
            if self.unique_keys:
                control_db = ControlMongodb(self.collection, self.unique_keys)
                result = await control_db.save_dataframe_to_collection(df)
            else:
                records = df.to_dict(orient="records")
                if records:
                    await self.collection.insert_many(records)
                result = {"success": True, "inserted": len(records), "updated": 0}
            
            total_inserted = result.get("inserted", 0) + result.get("updated", 0)
            message = f"批量更新完成，保存 {total_inserted} 条数据"
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)
            
            return {"success": True, "message": message, "inserted": total_inserted}
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
