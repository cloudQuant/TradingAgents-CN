"""
期货数据服务基类
提供通用的数据获取、更新、查询功能
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class BaseFuturesService:
    """期货数据服务基类"""
    
    def __init__(self, db: AsyncIOMotorClient, collection_name: str, provider):
        """
        初始化服务
        
        Args:
            db: MongoDB客户端
            collection_name: 集合名称
            provider: 数据提供者实例
        """
        self.db = db
        self.collection_name = collection_name
        self.collection = db[collection_name]
        self.provider = provider
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        
        latest = await self.collection.find_one(sort=[("更新时间", -1)])
        oldest = await self.collection.find_one(sort=[("更新时间", 1)])
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("更新时间") if latest else None,
            "oldest_date": oldest.get("更新时间") if oldest else None,
        }
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("更新时间", -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串
        for item in data:
            item["_id"] = str(item["_id"])
            if "更新时间" in item and isinstance(item["更新时间"], datetime):
                item["更新时间"] = item["更新时间"].isoformat()
        
        return {
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据
        子类可以重写此方法以实现特定的更新逻辑
        """
        try:
            logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 调用provider获取数据
            df = self.provider.fetch_data(**kwargs)
            
            if df is None or df.empty:
                logger.warning(f"[{self.collection_name}] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 使用ControlMongodb保存数据
            unique_keys = self.provider.get_unique_keys()
            extra_fields = {"数据源": "akshare", "接口名称": self.provider.akshare_func}
            
            control_db = ControlMongodb(self.collection, unique_keys)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "inserted": result.get("inserted", 0) + result.get("updated", 0),
                "details": result,
            }
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        默认实现调用单条更新，子类可以重写此方法实现批量逻辑
        """
        try:
            task_manager = get_task_manager() if task_id else None
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, 100, f"开始更新 {self.collection_name}...")
            
            # 默认调用单条更新
            result = await self.update_single_data(**kwargs)
            
            if task_manager and task_id:
                if result.get("success"):
                    task_manager.update_progress(task_id, 100, 100, f"更新完成: {result.get('message')}")
                    task_manager.complete_task(task_id, result=result)
                else:
                    task_manager.fail_task(task_id, result.get("message", "更新失败"))
            
            return result
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空集合数据"""
        try:
            result = await self.collection.delete_many({})
            return {
                "success": True,
                "deleted_count": result.deleted_count,
                "message": f"已删除 {result.deleted_count} 条数据"
            }
        except Exception as e:
            logger.error(f"[{self.collection_name}] 清空数据失败: {e}")
            return {
                "success": False,
                "message": str(e)
            }
