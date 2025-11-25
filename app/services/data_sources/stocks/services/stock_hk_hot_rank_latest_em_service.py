"""
港股服务
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.stock_hk_hot_rank_latest_em_provider import StockHkHotRankLatestEmProvider

logger = logging.getLogger(__name__)


class StockHkHotRankLatestEmService:
    """港股服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db.stocks.stock_hk_hot_rank_latest_em
        self.provider = StockHkHotRankLatestEmProvider()
        
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
    
    async def refresh_data(self, **kwargs) -> Dict[str, Any]:
        """刷新数据"""
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
                    "message": "Data refreshed successfully",
                    "inserted": len(result.inserted_ids),
                }
            
            return {
                "success": True,
                "message": "No operations performed",
                "inserted": 0,
            }
            
        except Exception as e:
            logger.error(f"Error refreshing data: {e}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空数据"""
        result = await self.collection.delete_many({})
        return {
            "success": True,
            "message": f"Deleted {result.deleted_count} records",
            "deleted": result.deleted_count,
        }
