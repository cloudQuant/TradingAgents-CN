"""
基金持仓变动-东财服务

参考文档: app/services/data_sources/funds/collection_config_ways.md
"""
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime
import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager
from ..providers.fund_portfolio_change_em_provider import FundPortfolioChangeEmProvider

logger = logging.getLogger(__name__)


class FundPortfolioChangeEmService:
    """基金持仓变动-东财服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["fund_portfolio_change_em"]
        self.provider = FundPortfolioChangeEmProvider()
        
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
        """更新单条数据（需要 fund_code 和 year 参数）"""
        try:
            logger.info(f"[fund_portfolio_change_em] update_single_data 收到参数: {kwargs}")
            fund_code = kwargs.get("fund_code") or kwargs.get("symbol") or kwargs.get("code")
            year = kwargs.get("year") or kwargs.get("date")
            logger.info(f"[fund_portfolio_change_em] 解析参数: fund_code={fund_code}, year={year}")
            
            # 参数验证
            if not fund_code:
                return {
                    "success": False,
                    "message": "缺少必须参数: fund_code（单条更新需要提供基金代码，如需批量更新请使用批量更新功能）",
                    "inserted": 0,
                }
            if not year:
                return {
                    "success": False,
                    "message": "缺少必须参数: year（请提供年份，如 2024）",
                    "inserted": 0,
                }
            
            logger.info(f"[fund_portfolio_change_em] 调用 provider.fetch_data(fund_code={fund_code}, year={year})")
            df = self.provider.fetch_data(fund_code=fund_code, year=year)
            
            if df is None or df.empty:
                logger.warning(f"[fund_portfolio_change_em] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 使用 ControlMongodb 处理数据去重
            unique_keys = ["基金代码", "股票代码", "季度"]
            extra_fields = {"数据源": "akshare", "接口名称": "fund_portfolio_change_em"}
            
            control_db = ControlMongodb(self.collection, unique_keys)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "inserted": result.get("inserted", 0) + result.get("updated", 0),
                "details": result,
            }
            
        except Exception as e:
            logger.error(f"[fund_portfolio_change_em] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新基金持仓变动数据
        
        Args:
            task_id: 任务ID，用于更新进度
            year: 年份参数（必填）
            concurrency: 并发数（默认3）
        """
        try:
            task_manager = get_task_manager() if task_id else None
            year = kwargs.get("year")
            concurrency = int(kwargs.get("concurrency", 3))
            
            # 年份必填
            if not year:
                if task_manager and task_id:
                    task_manager.fail_task(task_id, "缺少必须参数: year（批量更新需要指定年份）")
                return {
                    "success": False,
                    "message": "缺少必须参数: year（批量更新需要指定年份）",
                    "inserted": 0,
                }
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, 100, "正在从 fund_name_em 获取基金代码列表...")
            
            # 1. 从 fund_name_em 获取全部基金代码
            fund_codes: List[str] = []
            cursor = self.db["fund_name_em"].find({}, {"基金代码": 1})
            async for doc in cursor:
                code = doc.get("基金代码")
                if code:
                    fund_codes.append(code)
            
            if not fund_codes:
                if task_manager and task_id:
                    task_manager.fail_task(task_id, "fund_name_em 集合为空，请先更新基金基本信息")
                return {
                    "success": False,
                    "message": "fund_name_em 集合为空，请先更新基金基本信息",
                    "inserted": 0,
                }
            
            logger.info(f"[fund_portfolio_change_em] 从 fund_name_em 获取到 {len(fund_codes)} 个基金代码")
            
            # 2. 获取已存在的基金代码+年份组合
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, "正在检查已有数据，避免重复获取...")
            
            existing_combinations: Set[Tuple[str, str]] = set()
            existing_cursor = self.collection.find({}, {"基金代码": 1, "季度": 1})
            async for doc in existing_cursor:
                fund_code_db = doc.get("基金代码")
                quarter = str(doc.get("季度", ""))
                # 季度格式如 "2024年1季度"，提取年份
                if fund_code_db and len(quarter) >= 4 and quarter[:4].isdigit():
                    year_db = quarter[:4]
                    existing_combinations.add((fund_code_db, year_db))
            
            logger.info(f"[fund_portfolio_change_em] 已存在 {len(existing_combinations)} 个基金代码+年份组合")
            
            # 3. 生成待更新的组合（排除已存在的）
            combinations = [
                (code, str(year))
                for code in fund_codes
                if (code, str(year)) not in existing_combinations
            ]
            
            if not combinations:
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, "所有数据已存在，无需更新")
                    task_manager.complete_task(task_id)
                return {
                    "success": True,
                    "message": "所有数据已存在，无需更新",
                    "inserted": 0,
                }
            
            total_combinations = len(combinations)
            logger.info(f"[fund_portfolio_change_em] 需要更新 {total_combinations} 个基金代码+年份组合")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"需要更新 {total_combinations} 个组合，开始并发获取...")
            
            # 4. 使用信号量控制并发
            semaphore = asyncio.Semaphore(concurrency)
            total_inserted = 0
            processed = 0
            failed = 0
            lock = asyncio.Lock()
            
            async def fetch_and_save(code: str, y: str):
                nonlocal total_inserted, processed, failed
                async with semaphore:
                    try:
                        # 同步调用 provider（akshare 是同步的）
                        df = await asyncio.get_event_loop().run_in_executor(
                            None, 
                            lambda: self.provider.fetch_data(fund_code=code, year=y)
                        )
                        
                        if df is not None and not df.empty:
                            # 使用 ControlMongodb 保存数据，自动处理重复
                            unique_keys = ["基金代码", "股票代码", "季度"]
                            extra_fields = {"数据源": "akshare", "接口名称": "fund_portfolio_change_em"}
                            
                            control_db = ControlMongodb(self.collection, unique_keys)
                            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
                            
                            async with lock:
                                total_inserted += result.get("inserted", 0) + result.get("updated", 0)
                                processed += 1
                        else:
                            async with lock:
                                processed += 1
                                
                    except Exception as e:
                        logger.debug(f"获取基金 {code} 年份 {y} 持仓变动失败: {e}")
                        async with lock:
                            failed += 1
                            processed += 1
                    
                    # 更新进度
                    async with lock:
                        if task_manager and task_id and processed % 100 == 0:
                            progress = 10 + int((processed / total_combinations) * 85)
                            task_manager.update_progress(
                                task_id, progress, 100, 
                                f"已处理 {processed}/{total_combinations}，成功插入 {total_inserted} 条"
                            )
            
            # 5. 并发执行所有任务
            tasks = [fetch_and_save(code, y) for code, y in combinations]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 6. 完成
            message = f"批量更新完成，处理 {processed} 个组合，成功插入/更新 {total_inserted} 条，失败 {failed} 个"
            logger.info(f"[fund_portfolio_change_em] {message}")
            
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
            logger.error(f"[fund_portfolio_change_em] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
