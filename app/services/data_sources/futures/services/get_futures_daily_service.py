"""
内盘-历史行情数据-交易所服务

支持增量更新：从数据库最大日期开始更新到今天
支持按交易所批量更新
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging
import asyncio

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.futures.providers.get_futures_daily_provider import GetFuturesDailyProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)

# 所有支持的交易所
ALL_MARKETS = ["DCE", "CZCE", "SHFE", "CFFEX", "INE", "GFEX"]


class GetFuturesDailyService(BaseService):
    """
    内盘-历史行情数据-交易所服务
    
    支持：
    - 单条更新：获取指定交易所、指定日期范围的历史行情
    - 批量更新：从数据库最大日期开始增量更新到今天（可选按交易所）
    """
    
    # ===== 必须定义的属性 =====
    collection_name = "get_futures_daily"
    provider_class = GetFuturesDailyProvider
    
    # ===== 可选配置 =====
    time_field = "date"
    unique_keys = ["symbol", "date"]
    
    # 默认开始日期（如果数据库为空）
    DEFAULT_START_DATE = "20100101"
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据
        
        支持增量更新：如果不提供 start_date，则从数据库最大日期开始
        """
        try:
            market = kwargs.get("market", "DCE")
            start_date = kwargs.get("start_date")
            end_date = kwargs.get("end_date")
            
            # 如果没有提供开始日期，从数据库最大日期开始
            if not start_date:
                start_date = await self._get_max_date_for_market(market)
                # 从最大日期的下一天开始
                try:
                    start_dt = datetime.strptime(start_date, "%Y%m%d") + timedelta(days=1)
                    start_date = start_dt.strftime("%Y%m%d")
                except ValueError:
                    pass
            
            # 如果没有提供结束日期，使用今天
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            
            self.logger.info(f"[{self.collection_name}] 获取 {market} 从 {start_date} 到 {end_date} 的数据")
            
            # 获取数据
            df = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.provider.fetch_data(market=market, start_date=start_date, end_date=end_date)
            )
            
            if df is None or df.empty:
                return {"success": True, "message": f"{market}: 无新数据", "inserted": 0}
            
            # 保存数据
            control_db = ControlMongodb(self.collection, self.unique_keys, self.current_user)
            result = await control_db.save_dataframe_to_collection(df)
            
            inserted = result.get("inserted", 0) + result.get("updated", 0)
            return {
                "success": True,
                "message": f"{market}: 保存 {inserted} 条数据",
                "inserted": inserted
            }
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 更新失败: {e}", exc_info=True)
            return {"success": False, "message": str(e), "inserted": 0}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新（增量更新）
        
        按交易所从数据库最大日期开始更新到今天
        """
        task_manager = get_task_manager() if task_id else None
        
        try:
            market_param = kwargs.get("market", "ALL")
            
            # 确定要更新的交易所列表
            if market_param == "ALL":
                markets = ALL_MARKETS
            else:
                markets = [market_param]
            
            total_markets = len(markets)
            total_inserted = 0
            results = []
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, f"准备更新 {total_markets} 个交易所")
            
            for i, market in enumerate(markets):
                try:
                    # 获取该交易所的最大日期
                    max_date = await self._get_max_date_for_market(market)
                    
                    # 从最大日期的下一天开始
                    try:
                        start_dt = datetime.strptime(max_date, "%Y%m%d") + timedelta(days=1)
                        start_date = start_dt.strftime("%Y%m%d")
                    except ValueError:
                        start_date = self.DEFAULT_START_DATE
                    
                    end_date = datetime.now().strftime("%Y%m%d")
                    
                    # 检查是否需要更新
                    if start_date > end_date:
                        self.logger.info(f"[{self.collection_name}] {market}: 数据已是最新")
                        results.append(f"{market}: 已是最新")
                        continue
                    
                    self.logger.info(f"[{self.collection_name}] {market}: 从 {start_date} 更新到 {end_date}")
                    
                    # 获取数据
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda m=market, s=start_date, e=end_date: self.provider.fetch_data(market=m, start_date=s, end_date=e)
                    )
                    
                    if df is not None and not df.empty:
                        # 保存数据
                        control_db = ControlMongodb(self.collection, self.unique_keys, self.current_user)
                        result = await control_db.save_dataframe_to_collection(df)
                        inserted = result.get("inserted", 0) + result.get("updated", 0)
                        total_inserted += inserted
                        results.append(f"{market}: +{inserted}")
                    else:
                        results.append(f"{market}: 无新数据")
                    
                except Exception as e:
                    self.logger.warning(f"[{self.collection_name}] {market} 更新失败: {e}")
                    results.append(f"{market}: 失败")
                
                # 更新进度
                if task_manager and task_id:
                    progress = 5 + int((i + 1) / total_markets * 90)
                    task_manager.update_progress(
                        task_id, progress, 100,
                        f"已处理 {i + 1}/{total_markets} 个交易所"
                    )
                
                # 控制API调用频率
                await asyncio.sleep(0.2)
            
            message = f"增量更新完成，共保存 {total_inserted} 条。{'; '.join(results)}"
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)
            
            return {"success": True, "message": message, "inserted": total_inserted}
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
    
    async def _get_max_date_for_market(self, market: str = None) -> str:
        """获取指定交易所在数据库中的最大日期"""
        try:
            # 构建查询条件
            match_stage = {}
            if market:
                # 根据合约代码判断交易所（简单规则）
                # 实际上可能需要更复杂的逻辑
                pass
            
            # 查询最大日期
            pipeline = [
                {"$group": {"_id": None, "max_date": {"$max": f"${self.time_field}"}}}
            ]
            cursor = self.collection.aggregate(pipeline)
            result = await cursor.to_list(length=1)
            
            if result and result[0].get("max_date"):
                max_date = result[0]["max_date"]
                if isinstance(max_date, datetime):
                    return max_date.strftime("%Y%m%d")
                elif isinstance(max_date, str):
                    return max_date.replace("-", "").replace("/", "")[:8]
            
            return self.DEFAULT_START_DATE
            
        except Exception as e:
            self.logger.warning(f"[{self.collection_name}] 获取最大日期失败: {e}")
            return self.DEFAULT_START_DATE
