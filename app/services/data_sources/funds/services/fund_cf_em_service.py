"""
基金拆分-东财服务

参考文档: app/services/data_sources/funds/collection_config_ways.md
"""
from typing import Optional, Dict, Any, List, Set
from datetime import datetime
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager
from ..providers.fund_cf_em_provider import FundCfEmProvider

logger = logging.getLogger(__name__)


class FundCfEmService:
    """基金拆分-东财服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["fund_cf_em"]
        self.provider = FundCfEmProvider()
        
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
        """更新单条数据（需要 year 参数）"""
        try:
            logger.info(f"[fund_cf_em] update_single_data 收到参数: {kwargs}")
            year = kwargs.get("year") or kwargs.get("date")
            logger.info(f"[fund_cf_em] 解析参数: year={year}")
            
            # 参数验证
            if not year:
                return {
                    "success": False,
                    "message": "缺少必须参数: year（请提供年份，如 2020）",
                    "inserted": 0,
                }
            
            logger.info(f"[fund_cf_em] 调用 provider.fetch_data(year={year})")
            df = self.provider.fetch_data(year=year)
            
            if df is None or df.empty:
                logger.warning(f"[fund_cf_em] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 使用 ControlMongodb 处理数据去重
            unique_keys = ["基金代码", "拆分折算日", "年份"]
            extra_fields = {"数据源": "akshare", "接口名称": "fund_cf_em"}
            
            control_db = ControlMongodb(self.collection, unique_keys)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "inserted": result.get("inserted", 0) + result.get("updated", 0),
                "details": result,
            }
            
        except Exception as e:
            logger.error(f"[fund_cf_em] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新基金拆分数据
        
        Args:
            task_id: 任务ID，用于更新进度
            concurrency: 并发数（默认3）
        """
        try:
            task_manager = get_task_manager() if task_id else None
            concurrency = int(kwargs.get("concurrency", 3))
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, 100, "正在准备年份列表...")
            
            # 1. 生成年份范围（2005年到今年）
            current_year = datetime.now().year
            years = [str(y) for y in range(2005, current_year + 1)]
            
            logger.info(f"[fund_cf_em] 年份范围: {years[0]} - {years[-1]}")
            
            # 2. 获取已存在的年份（增量更新）
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, "正在检查已有数据，避免重复获取...")
            
            existing_years: Set[str] = set()
            existing_cursor = self.collection.find({}, {"年份": 1})
            async for doc in existing_cursor:
                y = doc.get("年份")
                if y:
                    existing_years.add(str(y))
            
            logger.info(f"[fund_cf_em] 已存在 {len(existing_years)} 个年份的数据")
            
            # 3. 生成待更新的年份（排除已存在的）
            years_to_update = [y for y in years if y not in existing_years]
            
            if not years_to_update:
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, "所有年份数据已存在，无需更新")
                    task_manager.complete_task(task_id)
                return {
                    "success": True,
                    "message": "所有年份数据已存在，无需更新",
                    "inserted": 0,
                }
            
            total_years = len(years_to_update)
            logger.info(f"[fund_cf_em] 需要更新 {total_years} 个年份")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"需要更新 {total_years} 个年份，开始并发获取...")
            
            # 4. 使用信号量控制并发
            semaphore = asyncio.Semaphore(concurrency)
            total_inserted = 0
            processed = 0
            failed = 0
            lock = asyncio.Lock()
            
            async def fetch_and_save(year: str):
                nonlocal total_inserted, processed, failed
                async with semaphore:
                    try:
                        # 同步调用 provider（akshare 是同步的）
                        df = await asyncio.get_event_loop().run_in_executor(
                            None, 
                            lambda: self.provider.fetch_data(year=year)
                        )
                        
                        if df is not None and not df.empty:
                            # 使用 ControlMongodb 保存数据，自动处理重复
                            unique_keys = ["基金代码", "拆分折算日", "年份"]
                            extra_fields = {"数据源": "akshare", "接口名称": "fund_cf_em"}
                            
                            control_db = ControlMongodb(self.collection, unique_keys)
                            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
                            
                            async with lock:
                                total_inserted += result.get("inserted", 0) + result.get("updated", 0)
                                processed += 1
                        else:
                            async with lock:
                                processed += 1
                                
                    except Exception as e:
                        logger.debug(f"获取年份 {year} 拆分数据失败: {e}")
                        async with lock:
                            failed += 1
                            processed += 1
                    
                    # 更新进度
                    async with lock:
                        if task_manager and task_id:
                            progress = 10 + int((processed / total_years) * 85)
                            task_manager.update_progress(
                                task_id, progress, 100, 
                                f"已处理 {processed}/{total_years} 个年份，成功插入 {total_inserted} 条"
                            )
            
            # 5. 并发执行所有任务
            tasks = [fetch_and_save(year) for year in years_to_update]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 6. 完成
            message = f"批量更新完成，处理 {processed} 个年份，成功插入/更新 {total_inserted} 条，失败 {failed} 个"
            logger.info(f"[fund_cf_em] {message}")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(
                    task_id, 
                    result={"inserted": total_inserted, "processed": processed, "failed": failed},
                    message=message
                )
            
            return {
                "success": True,
                "message": message,
                "inserted": total_inserted,
                "processed": processed,
                "failed": failed,
            }
            
        except Exception as e:
            logger.error(f"[fund_cf_em] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
