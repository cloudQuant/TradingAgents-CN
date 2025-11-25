"""
债券基础信息详情服务
"""
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.database.control_mongodb import ControlMongodb
from app.services.data_sources.bonds.providers.bond_info_detail_cm_provider import BondInfoDetailCmProvider
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class BondInfoDetailCmService:
    """债券基础信息详情服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["bond_info_detail_cm"]
        self.provider = BondInfoDetailCmProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        latest = await self.collection.find_one(sort=[("更新时间", -1)])
        return {"total_count": total_count, "last_updated": latest.get("更新时间") if latest else None}
    
    async def get_data(self, skip: int = 0, limit: int = 100, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("更新时间", -1)
        data = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        for item in data:
            item["_id"] = str(item["_id"])
        return {"data": data, "total": total, "skip": skip, "limit": limit}
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """单条更新"""
        try:
            bond_code = kwargs.get("bond_code") or kwargs.get("symbol")
            if not bond_code:
                return {"success": False, "message": "缺少必须参数: bond_code", "inserted": 0}
            
            df = self.provider.fetch_data(bond_code=bond_code)
            
            if df is None or df.empty:
                return {"success": True, "message": "No data available", "inserted": 0}
            
            unique_keys = ["查询代码"]
            control_db = ControlMongodb(self.collection, unique_keys)
            result = await control_db.save_dataframe_to_collection(df)
            
            return {"success": result["success"], "message": result["message"], "inserted": result.get("inserted", 0) + result.get("updated", 0)}
            
        except Exception as e:
            logger.error(f"[bond_info_detail_cm] update_single_data 发生错误: {str(e)}")
            return {"success": False, "message": str(e), "inserted": 0}

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新（从bond_info_cm获取代码列表）"""
        try:
            task_manager = get_task_manager() if task_id else None
            concurrency = int(kwargs.get("concurrency", 3))
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, "正在从 bond_info_cm 获取债券代码列表...")
            
            # 获取债券代码列表
            bond_codes: List[str] = []
            cursor = self.db["bond_info_cm"].find({"endpoint": "bond_info_cm"}, {"债券代码": 1})
            async for doc in cursor:
                code = doc.get("债券代码")
                if code:
                    bond_codes.append(code)
            
            if not bond_codes:
                if task_manager and task_id:
                    task_manager.fail_task(task_id, "bond_info_cm 集合为空，请先更新债券信息")
                return {"success": False, "message": "bond_info_cm 集合为空", "inserted": 0}
            
            # 获取已存在的代码
            existing: Set[str] = set()
            async for doc in self.collection.find({}, {"查询代码": 1}):
                existing.add(doc.get("查询代码"))
            
            # 过滤待更新列表
            to_update = [c for c in bond_codes if c not in existing]
            
            if not to_update:
                if task_manager and task_id:
                    task_manager.complete_task(task_id, message="所有数据已存在")
                return {"success": True, "message": "所有数据已存在", "inserted": 0}
            
            total = len(to_update)
            total_inserted = 0
            processed = 0
            failed = 0
            semaphore = asyncio.Semaphore(concurrency)
            lock = asyncio.Lock()
            
            async def fetch_and_save(code: str):
                nonlocal total_inserted, processed, failed
                async with semaphore:
                    try:
                        df = await asyncio.get_event_loop().run_in_executor(None, lambda: self.provider.fetch_data(bond_code=code))
                        if df is not None and not df.empty:
                            unique_keys = ["查询代码"]
                            control_db = ControlMongodb(self.collection, unique_keys)
                            result = await control_db.save_dataframe_to_collection(df)
                            async with lock:
                                total_inserted += result.get("inserted", 0) + result.get("updated", 0)
                                processed += 1
                        else:
                            async with lock:
                                processed += 1
                    except Exception as e:
                        logger.debug(f"获取 {code} 失败: {e}")
                        async with lock:
                            failed += 1
                            processed += 1
                    
                    async with lock:
                        if task_manager and task_id and processed % 50 == 0:
                            progress = 10 + int((processed / total) * 85)
                            task_manager.update_progress(task_id, progress, 100, f"已处理 {processed}/{total}")
            
            tasks = [fetch_and_save(c) for c in to_update]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            message = f"批量更新完成，处理 {processed}，成功 {total_inserted}，失败 {failed}"
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)
            
            return {"success": True, "message": message, "inserted": total_inserted}
            
        except Exception as e:
            logger.error(f"[bond_info_detail_cm] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
