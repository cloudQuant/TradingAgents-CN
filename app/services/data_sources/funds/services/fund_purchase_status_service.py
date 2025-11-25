"""
基金申购状态-东财服务
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.fund_purchase_status_provider import FundPurchaseStatusProvider

logger = logging.getLogger(__name__)


class FundPurchaseStatusService:
    """基金申购状态-东财服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["fund_purchase_status"]
        self.provider = FundPurchaseStatusProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
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
        """更新单条数据"""
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            records = df.to_dict('records')
            
            # 批量插入
            if records:
                result = await self.collection.insert_many(records)
                return {
                    "success": True,
                    "message": "Data updated successfully",
                    "inserted": len(result.inserted_ids),
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

    async def update_batch_data(self, **kwargs) -> Dict[str, Any]:
        """批量更新数据（暂未实现）"""
        logger.warning(f"{self.__class__.__name__}.update_batch_data: 批量更新功能暂未实现")
        return {
            "success": False,
            "message": "批量更新功能暂未实现",
            "warning": True,
        }
