"""
货币报价时间序列数据服务
"""
import asyncio
import math
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.currency_time_series_provider import CurrencyTimeSeriesProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class CurrencyTimeSeriesService:
    """货币报价时间序列数据服务"""
    
    # 唯一标识字段
    UNIQUE_KEYS = ["date"]
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["currency_time_series"]
        self.provider = CurrencyTimeSeriesProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        latest = await self.collection.find_one(sort=[("date", -1)])
        oldest = await self.collection.find_one(sort=[("date", 1)])
        
        return {
            "total_count": total_count,
            "last_updated": latest.get("date") if latest else None,
            "oldest_date": oldest.get("date") if oldest else None,
        }
    
    async def get_data(self, skip: int = 0, limit: int = 100, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("date", -1)
        data = []
        
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            cleaned_doc = {}
            for key, value in doc.items():
                if value is None:
                    continue
                if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                    continue
                cleaned_doc[key] = value
            data.append(cleaned_doc)
        
        total = await self.collection.count_documents(query)
        return {"data": data, "total": total, "skip": skip, "limit": limit}

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """更新单条数据"""
        try:
            start_date = kwargs.get("start_date")
            end_date = kwargs.get("end_date")
            
            if not start_date or not end_date:
                return {"success": False, "message": "缺少必须参数: start_date, end_date", "inserted": 0}
            
            df = self.provider.fetch_data(**kwargs)
            if df.empty:
                return {"success": True, "message": "No data available", "inserted": 0}
            
            records = df.to_dict('records')
            ops = []
            
            for record in records:
                date_val = record.get("date")
                if not date_val:
                    continue
                
                date_str = date_val.isoformat() if hasattr(date_val, 'isoformat') else str(date_val)
                doc = {"date": date_str, "updated_at": datetime.now().isoformat()}
                
                for key, value in record.items():
                    if key == "date" or value is None:
                        continue
                    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                        continue
                    try:
                        doc[key] = float(value)
                    except:
                        doc[key] = str(value)
                
                ops.append(UpdateOne(
                    {"date": date_str},
                    {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
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
        """批量更新时间序列数据"""
        task_manager = get_task_manager() if task_id else None
        api_key = kwargs.get("api_key")
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        base = kwargs.get("base", "USD")
        max_codes = int(kwargs.get("max_codes", 100))
        batch_size = int(kwargs.get("batch_size", 20))
        
        if not api_key:
            msg = "缺少必须参数: api_key"
            if task_manager:
                task_manager.fail_task(task_id, msg)
            return {"success": False, "message": msg}
        
        if not start_date or not end_date:
            msg = "缺少必须参数: start_date, end_date"
            if task_manager:
                task_manager.fail_task(task_id, msg)
            return {"success": False, "message": msg}
        
        try:
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
                msg = "No currency codes found"
                if task_manager:
                    task_manager.fail_task(task_id, msg)
                return {"success": False, "message": msg}
            
            total_saved = 0
            total_batches = (len(codes) + batch_size - 1) // batch_size
            
            for batch_idx, i in enumerate(range(0, len(codes), batch_size)):
                if task_manager:
                    progress = int((batch_idx / total_batches) * 100)
                    task_manager.update_progress(task_id, progress, 100, f"处理第 {batch_idx + 1}/{total_batches} 批...")
                
                batch_codes = codes[i:i + batch_size]
                symbols = ",".join(batch_codes)
                
                try:
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda s=symbols: self.provider.fetch_data(
                            base=base, start_date=start_date, end_date=end_date, symbols=s, api_key=api_key
                        )
                    )
                    
                    if df is not None and not df.empty:
                        result = await self._save_records(df.to_dict('records'))
                        total_saved += result
                except Exception as e:
                    logger.error(f"Error in batch {batch_idx + 1}: {e}")
            
            message = f"批量同步完成，共保存 {total_saved} 条数据"
            if task_manager:
                task_manager.complete_task(task_id, result={"saved": total_saved}, message=message)
            
            return {"success": True, "message": message, "inserted": total_saved}
            
        except Exception as e:
            logger.error(f"Batch update failed: {e}")
            if task_manager:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}

    async def _save_records(self, records: list) -> int:
        """保存记录"""
        ops = []
        for record in records:
            date_val = record.get("date")
            if not date_val:
                continue
            date_str = date_val.isoformat() if hasattr(date_val, 'isoformat') else str(date_val)
            doc = {"date": date_str, "updated_at": datetime.now().isoformat()}
            for key, value in record.items():
                if key == "date" or value is None:
                    continue
                if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                    continue
                try:
                    doc[key] = float(value)
                except:
                    doc[key] = str(value)
            ops.append(UpdateOne({"date": date_str}, {"$set": doc}, upsert=True))
        
        if ops:
            result = await self.collection.bulk_write(ops, ordered=False)
            return (result.upserted_count or 0) + (result.modified_count or 0)
        return 0

    async def clear_data(self) -> Dict[str, Any]:
        """清空集合数据"""
        result = await self.collection.delete_many({})
        return {"success": True, "message": f"Cleared {result.deleted_count} records", "deleted": result.deleted_count}
