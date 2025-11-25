"""
期权数据服务基类
所有期权数据服务都应该继承此类
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


class BaseOptionService:
    """期权数据服务基类"""
    
    # 子类需要定义的属性
    collection_name: str = ""
    display_name: str = ""
    provider_class = None  # Provider类
    
    # 唯一键字段（用于upsert操作）
    unique_fields: List[str] = []
    
    def __init__(self, db: AsyncIOMotorDatabase, task_manager=None):
        self.db = db
        self.task_manager = task_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 初始化provider
        if self.provider_class:
            self.provider = self.provider_class()
        else:
            self.provider = None
    
    def get_collection(self):
        """获取MongoDB集合"""
        return self.db[self.collection_name]
    
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        collection = self.get_collection()
        count = await collection.count_documents({})
        
        # 获取最后更新时间
        last_doc = await collection.find_one(
            {"更新时间": {"$exists": True}},
            sort=[("更新时间", -1)]
        )
        last_update = last_doc.get("更新时间") if last_doc else None
        
        return {
            "collection_name": self.collection_name,
            "display_name": self.display_name,
            "total_count": count,
            "last_update": last_update
        }
    
    async def get_data(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict] = None,
        sort_field: Optional[str] = None,
        sort_order: int = -1
    ) -> Dict[str, Any]:
        """获取分页数据"""
        collection = self.get_collection()
        
        query = filters or {}
        skip = (page - 1) * page_size
        
        # 构建排序
        sort_spec = [(sort_field, sort_order)] if sort_field else [("_id", -1)]
        
        # 获取总数
        total = await collection.count_documents(query)
        
        # 获取数据
        cursor = collection.find(query).sort(sort_spec).skip(skip).limit(page_size)
        data = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            data.append(doc)
        
        return {
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据
        子类应该重写此方法实现具体的更新逻辑
        """
        raise NotImplementedError("子类必须实现 update_single_data 方法")
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        子类应该重写此方法实现具体的更新逻辑
        """
        raise NotImplementedError("子类必须实现 update_batch_data 方法")
    
    async def _save_data(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        保存数据到数据库
        使用upsert策略，根据unique_fields判断是否更新
        """
        if not records:
            return {"inserted": 0, "updated": 0}
        
        collection = self.get_collection()
        inserted = 0
        updated = 0
        
        for record in records:
            # 添加更新时间
            record['更新时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建查询条件
            if self.unique_fields:
                query = {field: record.get(field) for field in self.unique_fields if record.get(field)}
                if query:
                    result = await collection.update_one(
                        query,
                        {"$set": record},
                        upsert=True
                    )
                    if result.upserted_id:
                        inserted += 1
                    elif result.modified_count > 0:
                        updated += 1
                    continue
            
            # 没有唯一键，直接插入
            await collection.insert_one(record)
            inserted += 1
        
        return {"inserted": inserted, "updated": updated}
    
    async def _update_task_progress(self, task_id: str, current: int, total: int, message: str = ""):
        """更新任务进度"""
        if self.task_manager and task_id:
            progress = int((current / total) * 100) if total > 0 else 0
            await self.task_manager.update_task(
                task_id,
                progress=progress,
                message=message
            )
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空集合数据"""
        collection = self.get_collection()
        result = await collection.delete_many({})
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "message": f"已删除 {result.deleted_count} 条数据"
        }
    
    async def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        collection = self.get_collection()
        count = await collection.count_documents({})
        
        return {
            "total_count": count,
            "collection_name": self.collection_name
        }
