"""
货币转换数据服务
"""
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient

from ..providers.currency_convert_provider import CurrencyConvertProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class CurrencyConvertService:
    """货币转换数据服务"""
    
    # 唯一标识字段
    UNIQUE_KEYS = ["date", "base", "to", "amount"]
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["currency_convert"]
        self.provider = CurrencyConvertProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        # 统计不同货币对的数量
        pipeline = [
            {"$group": {"_id": {"base": "$base", "to": "$to"}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 20}
        ]
        pair_stats = await self.collection.aggregate(pipeline).to_list(length=20)
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
            "pair_stats": pair_stats,
        }
    
    async def get_data(self, skip: int = 0, limit: int = 100, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("scraped_at", -1)
        data = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {"data": data, "total": total, "skip": skip, "limit": limit}

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """更新单条数据（执行一次货币转换）"""
        try:
            base = kwargs.get("base", "USD")
            to = kwargs.get("to", "CNY")
            amount = kwargs.get("amount", "1")
            
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {"success": True, "message": "No data available", "inserted": 0}
            
            # 使用 ControlMongodb 进行数据去重
            control_db = ControlMongodb(self.collection, self.UNIQUE_KEYS)
            result = await control_db.save_dataframe_to_collection(
                df,
                extra_fields={
                    "数据源": "akshare",
                    "接口名称": "currency_convert"
                }
            )
            
            return {
                "success": True,
                "message": f"转换完成: {amount} {base} -> {to}",
                "inserted": result.get("upserted", 0) + result.get("modified", 0),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error updating single data: {e}")
            return {"success": False, "message": str(e), "inserted": 0}

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新货币转换数据
        
        Args:
            task_id: 任务ID
            api_key: API密钥
            pairs: 货币对列表，格式如 [{"base": "USD", "to": "CNY", "amount": "1000"}]
            concurrency: 并发数
        """
        task_manager = get_task_manager() if task_id else None
        api_key = kwargs.get("api_key")
        pairs = kwargs.get("pairs", [])
        concurrency = int(kwargs.get("concurrency", 2))
        
        if not api_key:
            msg = "缺少必须参数: api_key"
            if task_manager:
                task_manager.fail_task(task_id, msg)
            return {"success": False, "message": msg}
        
        # 默认货币对
        if not pairs:
            pairs = [
                {"base": "USD", "to": "CNY", "amount": "1"},
                {"base": "CNY", "to": "USD", "amount": "1"},
                {"base": "EUR", "to": "CNY", "amount": "1"},
                {"base": "GBP", "to": "CNY", "amount": "1"},
                {"base": "JPY", "to": "CNY", "amount": "100"},
            ]
        
        total_saved = 0
        success_count = 0
        failed_count = 0
        semaphore = asyncio.Semaphore(concurrency)
        
        async def fetch_and_save(pair: Dict, idx: int):
            nonlocal total_saved, success_count, failed_count
            async with semaphore:
                try:
                    base = pair.get("base", "USD")
                    to = pair.get("to", "CNY")
                    amount = pair.get("amount", "1")
                    
                    if task_manager:
                        progress = int((idx / len(pairs)) * 100)
                        task_manager.update_progress(task_id, progress, 100, f"转换 {amount} {base} -> {to}...")
                    
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: self.provider.fetch_data(base=base, to=to, amount=amount, api_key=api_key)
                    )
                    
                    if df is not None and not df.empty:
                        control_db = ControlMongodb(self.collection, self.UNIQUE_KEYS)
                        result = await control_db.save_dataframe_to_collection(df)
                        count = result.get("upserted", 0) + result.get("modified", 0)
                        total_saved += count
                        success_count += 1
                        
                except Exception as e:
                    logger.error(f"Error converting {pair}: {e}")
                    failed_count += 1
        
        try:
            await asyncio.gather(*[fetch_and_save(pair, idx) for idx, pair in enumerate(pairs)])
            
            message = f"批量转换完成: 成功 {success_count}/{len(pairs)}, 共保存 {total_saved} 条数据"
            
            if task_manager:
                task_manager.complete_task(
                    task_id,
                    result={"saved": total_saved, "success": success_count, "failed": failed_count},
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
