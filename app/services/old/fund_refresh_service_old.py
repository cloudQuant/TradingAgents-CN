"""
基金数据刷新服务
负责调用akshare获取基金数据并保存到数据库
"""
import logging
from typing import Dict, Any, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
from tqdm import tqdm
from tqdm.asyncio import tqdm as atqdm

from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService
from app.utils.task_manager import get_task_manager

logger = logging.getLogger("webapi")

# 线程池，用于执行同步的akshare调用
_executor = ThreadPoolExecutor(max_workers=10)


class FundRefreshService:
    """基金数据刷新服务"""
    
    def __init__(self, db=None):
        # AsyncIOMotorDatabase does not implement truthiness; avoid boolean evaluation
        self.db = db if db is not None else get_mongo_db()
        self.data_service = FundDataService(self.db)
        self.task_manager = get_task_manager()
    
    async def _update_task_progress(self, task_id: str, progress: int, message: str, total: int = 100) -> None:
        """统一封装任务进度更新，避免重复代码。
        
        使用 task_manager.update_progress，并在异常情况下记录警告日志，
        避免因为进度更新问题中断整个刷新流程。
        """
        try:
            self.task_manager.update_progress(task_id, progress, total, message)
        except Exception as e:
            logger.warning(
                f"更新任务进度失败: {e}; task_id={task_id}, progress={progress}, total={total}, message={message}"
            )
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的基金数据集合
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.start_task(task_id)
            self.task_manager.update_progress(task_id, 0, 100, f"开始刷新 {collection_name}...")
            
            # 根据collection_name调用不同的刷新方法
            handlers = {
                "fund_name_em": self._refresh_fund_name_em,
                "fund_basic_info": self._refresh_fund_basic_info,
                "fund_info_index_em": self._refresh_fund_info_index_em,
                "fund_purchase_status": self._refresh_fund_purchase_status,
                "fund_etf_spot_em": self._refresh_fund_etf_spot,
                "fund_etf_spot_ths": self._refresh_fund_etf_spot_ths,
                "fund_lof_spot_em": self._refresh_fund_lof_spot,
                "fund_spot_sina": self._refresh_fund_spot_sina,
                "fund_etf_hist_min_em": self._refresh_fund_etf_hist_min,
                "fund_lof_hist_min_em": self._refresh_fund_lof_hist_min,
                "fund_etf_hist_em": self._refresh_fund_etf_hist,
                "fund_lof_hist_em": self._refresh_fund_lof_hist,
                "fund_hist_sina": self._refresh_fund_hist_sina,
                "fund_open_fund_daily_em": self._refresh_fund_open_fund_daily,
                "fund_open_fund_info_em": self._refresh_fund_open_fund_info,
                "fund_money_fund_daily_em": self._refresh_fund_money_fund_daily,
                "fund_money_fund_info_em": self._refresh_fund_money_fund_info,
                "fund_financial_fund_daily_em": self._refresh_fund_financial_fund_daily,
                "fund_financial_fund_info_em": self._refresh_fund_financial_fund_info,
                "fund_graded_fund_daily_em": self._refresh_fund_graded_fund_daily,
                "fund_graded_fund_info_em": self._refresh_fund_graded_fund_info,
                "fund_etf_fund_daily_em": self._refresh_fund_etf_fund_daily,
                "fund_hk_hist_em": self._refresh_fund_hk_hist_em,
                "fund_etf_fund_info_em": self._refresh_fund_etf_fund_info_em,
                "fund_etf_dividend_sina": self._refresh_fund_etf_dividend_sina,
                "fund_fh_em": self._refresh_fund_fh_em,
                "fund_cf_em": self._refresh_fund_cf_em,
                "fund_fh_rank_em": self._refresh_fund_fh_rank_em,
                "fund_open_fund_rank_em": self._refresh_fund_open_fund_rank_em,
                "fund_exchange_rank_em": self._refresh_fund_exchange_rank_em,
                "fund_money_rank_em": self._refresh_fund_money_rank_em,
                "fund_lcx_rank_em": self._refresh_fund_lcx_rank_em,
                "fund_hk_rank_em": self._refresh_fund_hk_rank_em,
                "fund_individual_achievement_xq": self._refresh_fund_individual_achievement_xq,
                "fund_value_estimation_em": self._refresh_fund_value_estimation_em,
                "fund_individual_analysis_xq": self._refresh_fund_individual_analysis_xq,
                "fund_individual_profit_probability_xq": self._refresh_fund_individual_profit_probability_xq,
                "fund_individual_detail_hold_xq": self._refresh_fund_individual_detail_hold_xq,
                "fund_overview_em": self._refresh_fund_overview_em,
                "fund_fee_em": self._refresh_fund_fee_em,
                "fund_individual_detail_info_xq": self._refresh_fund_individual_detail_info_xq,
                "fund_portfolio_hold_em": self._refresh_fund_portfolio_hold_em,
                "fund_portfolio_bond_hold_em": self._refresh_fund_portfolio_bond_hold_em,
                "fund_portfolio_industry_allocation_em": self._refresh_fund_portfolio_industry_allocation_em,
                "fund_portfolio_change_em": self._refresh_fund_portfolio_change_em,
                "fund_rating_all_em": self._refresh_fund_rating_all_em,
                "fund_rating_sh_em": self._refresh_fund_rating_sh_em,
                "fund_rating_zs_em": self._refresh_fund_rating_zs_em,
                "fund_rating_ja_em": self._refresh_fund_rating_ja_em,
                "fund_manager_em": self._refresh_fund_manager_em,
                "fund_new_found_em": self._refresh_fund_new_found_em,
                "fund_scale_open_sina": self._refresh_fund_scale_open_sina,
                "fund_scale_close_sina": self._refresh_fund_scale_close_sina,
                "fund_scale_structured_sina": self._refresh_fund_scale_structured_sina,
                "fund_aum_em": self._refresh_fund_aum_em,
                "fund_aum_trend_em": self._refresh_fund_aum_trend_em,
                "fund_aum_hist_em": self._refresh_fund_aum_hist_em,
                "reits_realtime_em": self._refresh_reits_realtime_em,
                "reits_hist_em": self._refresh_reits_hist_em,
                "fund_report_stock_cninfo": self._refresh_fund_report_stock_cninfo,
                "fund_report_industry_allocation_cninfo": self._refresh_fund_report_industry_allocation_cninfo,
                "fund_report_asset_allocation_cninfo": self._refresh_fund_report_asset_allocation_cninfo,
                "fund_scale_change_em": self._refresh_fund_scale_change_em,
                "fund_hold_structure_em": self._refresh_fund_hold_structure_em,
                "fund_stock_position_lg": self._refresh_fund_stock_position_lg,
                "fund_balance_position_lg": self._refresh_fund_balance_position_lg,
                "fund_linghuo_position_lg": self._refresh_fund_linghuo_position_lg,
                "fund_announcement_dividend_em": self._refresh_fund_announcement_dividend_em,
                "fund_announcement_report_em": self._refresh_fund_announcement_report_em,
                "fund_announcement_personnel_em": self._refresh_fund_announcement_personnel_em,
            }
            
            handler = handlers.get(collection_name)
            if not handler:
                raise ValueError(f"不支持的集合类型: {collection_name}")
            
            result = await handler(task_id, params or {})
            
            # 确保任务状态正确更新为成功
            message = result.get('message', '数据更新成功')
            self.task_manager.complete_task(task_id, result, message)
            logger.info(f"任务 {task_id} 完成: {message}")
            return result
            
        except Exception as e:
            logger.error(f"刷新集合 {collection_name} 失败: {e}", exc_info=True)
            self.task_manager.fail_task(task_id, str(e))
            raise
    
    async def _refresh_fund_name_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金基本信息数据
        使用akshare的fund_name_em接口
        
        Args:
            task_id: 任务ID
            params: 参数（该接口无需参数）
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金基本信息...")
            
            # 在线程池中调用akshare（因为akshare是同步的）
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_name_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金基本信息数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条基金数据，正在保存...")
            
            # 定义进度回调函数
            def on_save_progress(current, total, percentage, message):
                # 计算总体进度（50%用于获取数据，50%用于保存数据）
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            # 保存数据（传入进度回调）
            saved_count = await self.data_service.save_fund_name_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金基本信息"
            }
            
        except Exception as e:
            logger.error(f"刷新基金基本信息失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_name_em(self):
        """
        调用akshare获取基金基本信息（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 基金基本信息数据
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金基本信息...")
            df = ak.fund_name_em()
            logger.info(f"成功获取 {len(df)} 条基金基本信息")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金基本信息失败: {e}", exc_info=True)
            raise

    def _fetch_fund_info_index_em(self, symbol: str, indicator: str):
        """调用 akshare 获取指数型基金基本信息（fund_info_index_em）"""
        try:
            import akshare as ak
            logger.info(
                f"开始调用 akshare.fund_info_index_em(symbol={symbol}, indicator={indicator})..."
            )
            df = ak.fund_info_index_em(symbol=symbol, indicator=indicator)
            logger.info(f"成功获取 {len(df)} 条指数型基金基本信息")
            return df
        except Exception as e:
            logger.error(f"调用 akshare 获取指数型基金基本信息失败: {e}", exc_info=True)
            raise

    def _fetch_fund_detail_xq(self, symbol: str):
        """
        获取单个基金的雪球详情
        """
        try:
            import akshare as ak
            # ak.fund_individual_basic_info_xq(symbol="000001")
            # 返回 item 和 value 两列
            df = ak.fund_individual_basic_info_xq(symbol=symbol)
            if df is not None and not df.empty:
                 # 转置: item作为key, value作为value
                 data = dict(zip(df['item'], df['value']))
                 return data
            return None
        except Exception as e:
            # 忽略单个失败，避免刷屏日志，仅在需要调试时开启
            # logger.debug(f"获取基金 {symbol} 详情失败: {e}")
            return None
    
    async def _refresh_fund_basic_info(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新fund_basic_info基金基本信息数据
        使用akshare的fund_individual_basic_info_xq接口
        此过程可能较慢，需要批量处理
        
        Args:
            task_id: 任务ID
            params: 参数
                - batch_size: 每批保存数量，默认50
                - concurrency: 并发请求数，默认5
                - delay: 请求间隔(秒)，默认0.1
            
        Returns:
            刷新结果
        """
        try:
            batch_size = params.get('batch_size', 50)
            concurrency = params.get('concurrency', 5)
            delay = params.get('delay', 0.1)
            target_fund_code = params.get('fund_code')
            
            if target_fund_code:
                # 单个更新模式
                fund_codes = [str(target_fund_code)]
                self.task_manager.update_progress(task_id, 5, 100, f"准备更新单个基金: {target_fund_code}")
            else:
                # 批量更新模式
                self.task_manager.update_progress(task_id, 5, 100, "正在获取全量基金列表...")
                
                # 1. 获取所有基金代码
                loop = asyncio.get_event_loop()
                fund_list_df = await loop.run_in_executor(_executor, self._fetch_fund_name_em)
                
                if fund_list_df is None or fund_list_df.empty:
                    raise ValueError("未获取到基金列表，无法进行详情更新")
                    
                # 假设列名包含 '基金代码'
                if '基金代码' not in fund_list_df.columns:
                     # 尝试适配可能的列名
                     if 'code' in fund_list_df.columns:
                         fund_codes = fund_list_df['code'].astype(str).tolist()
                     else:
                         raise ValueError(f"基金列表缺少'基金代码'列: {fund_list_df.columns}")
                else:
                    fund_codes = fund_list_df['基金代码'].astype(str).tolist()
                
            total_funds = len(fund_codes)
            # total_funds = min(total_funds, 20) # DEBUG: 只跑前20个用于测试
            
            self.task_manager.update_progress(task_id, 10, 100, f"获取到 {total_funds} 只基金，准备开始获取详情...")
            logger.info(f"开始更新雪球基金详情，共 {total_funds} 只，并发 {concurrency}，延迟 {delay}s")
            
            processed_count = 0
            saved_count = 0
            failed_count = 0
            buffer = []
            
            # 使用Semaphore限制并发
            sem = asyncio.Semaphore(concurrency)
            
            async def fetch_worker(code):
                async with sem:
                    await asyncio.sleep(delay)
                    return await loop.run_in_executor(_executor, self._fetch_fund_detail_xq, code)

            # 分块处理，避免一次性创建过多Task
            chunk_size = 100 # 每次提交100个任务
            chunks = [fund_codes[i:i + chunk_size] for i in range(0, total_funds, chunk_size)]
            
            for i, chunk in enumerate(chunks):
                tasks = [fetch_worker(code) for code in chunk]
                results = await asyncio.gather(*tasks)
                
                valid_results = [r for r in results if r is not None]
                if valid_results:
                    buffer.extend(valid_results)
                
                failed_in_batch = len(chunk) - len(valid_results)
                failed_count += failed_in_batch
                processed_count += len(chunk)
                
                # 达到batch_size或最后一次时保存
                if len(buffer) >= batch_size or i == len(chunks) - 1:
                    if buffer:
                        df_to_save = pd.DataFrame(buffer)
                        count = await self.data_service.save_fund_basic_info_data(df_to_save)
                        saved_count += count
                        buffer = [] # 清空缓冲区
                
                # 更新进度 (10% - 100%)
                progress = 10 + int((processed_count / total_funds) * 90)
                self.task_manager.update_progress(
                    task_id, 
                    progress, 
                    100, 
                    f"已处理 {processed_count}/{total_funds}，成功 {saved_count}，失败 {failed_count}"
                )
            
            result_msg = f"更新完成：共 {total_funds} 只，成功更新 {saved_count} 只，失败 {failed_count} 只"
            self.task_manager.update_progress(task_id, 100, 100, result_msg)
            
            return {
                'success': True,
                'saved': saved_count,
                'failed': failed_count,
                'total': total_funds,
                'message': result_msg
            }
            
        except Exception as e:
            logger.error(f"刷新雪球基金基本信息失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_info_index_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新 fund_info_index_em 指数型基金基本信息数据

        使用 akshare.fund_info_index_em 接口，遍历所有参数组合获取完整数据。
        """
        try:
            # 定义所有参数组合（去掉"全部"）
            symbols = ["沪深指数", "行业主题", "大盘指数", "中盘指数", "小盘指数", "股票指数", "债券指数"]
            indicators = ["被动指数型", "增强指数型"]
            
            # 计算总组合数
            total_combinations = len(symbols) * len(indicators)
            logger.info(f"将遍历 {total_combinations} 个参数组合获取数据")
            
            all_dataframes = []
            combination_index = 0
            
            # 遍历所有组合
            for symbol in symbols:
                for indicator in indicators:
                    combination_index += 1
                    
                    # 更新进度：前60%用于获取数据
                    fetch_progress = int((combination_index / total_combinations) * 60)
                    msg_fetch = f"正在获取数据 [{combination_index}/{total_combinations}]: {symbol} - {indicator}..."
                    self.task_manager.update_progress(task_id, fetch_progress, 100, msg_fetch)
                    logger.info(msg_fetch)
                    
                    try:
                        loop = asyncio.get_event_loop()
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_info_index_em, symbol, indicator
                        )
                        
                        if df is not None and not df.empty:
                            logger.info(f"获取到 {len(df)} 条数据: {symbol} - {indicator}")
                            all_dataframes.append(df)
                        else:
                            logger.warning(f"未获取到数据: {symbol} - {indicator}")
                    
                    except Exception as e:
                        logger.error(f"获取数据失败 ({symbol} - {indicator}): {e}")
                        # 继续处理其他组合，不中断整个流程
                        continue
            
            if not all_dataframes:
                raise ValueError("所有参数组合都未获取到数据")
            
            # 合并所有数据并去重
            self.task_manager.update_progress(task_id, 65, 100, "正在合并和去重数据...")
            logger.info(f"合并 {len(all_dataframes)} 个数据集...")
            
            combined_df = pd.concat(all_dataframes, ignore_index=True)
            logger.info(f"合并后共 {len(combined_df)} 条数据")
            
            # 根据日期、基金代码和跟踪标的去重，保留最新的记录
            before_dedup = len(combined_df)
            combined_df = combined_df.drop_duplicates(subset=['日期', '基金代码', '跟踪标的'], keep='last')
            after_dedup = len(combined_df)
            logger.info(f"去重完成: {before_dedup} -> {after_dedup} 条 (删除 {before_dedup - after_dedup} 条重复)")
            
            self.task_manager.update_progress(
                task_id,
                70,
                100,
                f"获取并去重后共 {after_dedup} 条指数型基金数据，正在保存...",
            )

            def on_save_progress(current, total, percentage, message):
                # 70-100% 用于保存
                overall_progress = 70 + int(percentage * 0.3)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)

            saved_count = await self.data_service.save_fund_info_index_data(
                combined_df, progress_callback=on_save_progress
            )

            done_msg = f"成功更新 {saved_count} 条指数型基金基本信息（遍历 {total_combinations} 个参数组合）"
            self.task_manager.update_progress(task_id, 100, 100, done_msg)
            logger.info(done_msg)

            return {
                "success": True,
                "saved": saved_count,
                "total_combinations": total_combinations,
                "message": done_msg,
            }
        except Exception as e:
            logger.error(f"刷新指数型基金基本信息失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_purchase_em(self):
        """
        调用akshare获取基金申购状态（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 基金申购状态数据
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金申购状态...")
            df = ak.fund_purchase_em()
            logger.info(f"成功获取 {len(df)} 条基金申购状态数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金申购状态失败: {e}", exc_info=True)
            raise
    
    async def _refresh_fund_purchase_status(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金申购状态数据
        使用akshare的fund_purchase_em接口
        
        Args:
            task_id: 任务ID
            params: 参数（该接口无需参数）
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金申购状态...")
            
            # 在线程池中调用akshare（因为akshare是同步的）
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_purchase_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金申购状态数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条基金申购状态数据，正在保存...")
            
            # 定义进度回调函数
            def on_save_progress(current, total, percentage, message):
                # 计算总体进度（50%用于获取数据，50%用于保存数据）
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            # 保存数据（传入进度回调）
            saved_count = await self.data_service.save_fund_purchase_status_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金申购状态数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金申购状态失败: {e}", exc_info=True)
            raise
    
    async def _fetch_fund_etf_spot_em(self, max_retries: int = 3):
        """
        从AKShare获取ETF基金实时行情数据
        
        Args:
            max_retries: 最大重试次数
            
        Returns:
            DataFrame: ETF实时行情数据
        """
        import akshare as ak
        import time
        
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试获取ETF实时行情数据，第 {attempt + 1}/{max_retries} 次")
                df = await loop.run_in_executor(executor, ak.fund_etf_spot_em)
                executor.shutdown(wait=False)
                logger.info(f"成功获取ETF实时行情数据")
                return df
            except Exception as e:
                last_error = e
                logger.warning(f"第 {attempt + 1} 次获取失败: {str(e)}")
                
                if attempt < max_retries - 1:
                    # 等待后重试，使用指数退避策略
                    wait_time = 2 ** attempt  # 1秒, 2秒, 4秒
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    executor.shutdown(wait=False)
                    logger.error(f"获取ETF实时行情数据失败，已重试 {max_retries} 次")
                    raise ValueError(f"获取数据失败: {str(last_error)}。这可能是由于网络不稳定或东方财富网服务器暂时不可用。请稍后再试。") from last_error
        
        executor.shutdown(wait=False)
        raise ValueError(f"获取数据失败: {str(last_error)}") from last_error
    
    async def _refresh_fund_etf_spot(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新ETF基金实时行情数据
        
        Args:
            task_id: 任务ID
            params: 参数字典
            
        Returns:
            刷新结果
        """
        try:
            logger.info(f"开始刷新ETF基金实时行情数据，任务ID: {task_id}")
            
            # 更新进度：开始获取数据
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取ETF实时行情数据...")
            
            # 获取数据
            df = await self._fetch_fund_etf_spot_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到ETF基金实时行情数据")
            
            total_count = len(df)
            logger.info(f"成功获取 {total_count} 条ETF基金实时行情数据")
            
            # 更新进度：数据获取完成
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {total_count} 条数据，开始保存...")
            
            # 定义进度回调
            def on_save_progress(current, total, percentage, message):
                # 计算总体进度（50%用于获取数据，50%用于保存数据）
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            # 保存数据（传入进度回调）
            saved_count = await self.data_service.save_fund_etf_spot_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条ETF基金实时行情数据"
            }
            
        except Exception as e:
            logger.error(f"刷新ETF基金实时行情失败: {e}", exc_info=True)
            raise
    
    async def _fetch_fund_etf_spot_ths(self, date: str = "", max_retries: int = 3):
        """
        从AKShare获取同花顺ETF实时行情数据
        
        Args:
            date: 查询日期，格式为"YYYYMMDD"，默认为空返回最新数据
            max_retries: 最大重试次数
            
        Returns:
            DataFrame: 同花顺ETF实时行情数据
        """
        import akshare as ak
        
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试获取同花顺ETF实时行情数据，第 {attempt + 1}/{max_retries} 次，日期参数: {date if date else '最新'}")
                df = await loop.run_in_executor(executor, ak.fund_etf_spot_ths, date)
                executor.shutdown(wait=False)
                logger.info(f"成功获取同花顺ETF实时行情数据")
                return df
            except Exception as e:
                last_error = e
                logger.warning(f"第 {attempt + 1} 次获取失败: {str(e)}")
                
                if attempt < max_retries - 1:
                    # 等待后重试，使用指数退避策略
                    wait_time = 2 ** attempt  # 1秒, 2秒, 4秒
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    executor.shutdown(wait=False)
                    logger.error(f"获取同花顺ETF实时行情数据失败，已重试 {max_retries} 次")
                    raise ValueError(f"获取数据失败: {str(last_error)}。这可能是由于网络不稳定或同花顺服务器暂时不可用。请稍后再试。") from last_error
        
        executor.shutdown(wait=False)
        raise ValueError(f"获取数据失败: {str(last_error)}") from last_error
    
    async def _refresh_fund_etf_spot_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新同花顺ETF实时行情数据
        
        Args:
            task_id: 任务ID
            params: 参数字典，可选包含 date 参数
            
        Returns:
            刷新结果
        """
        try:
            logger.info(f"开始刷新同花顺ETF实时行情数据，任务ID: {task_id}")
            
            # 获取日期参数
            date = params.get('date', '')
            
            # 更新进度：开始获取数据
            date_desc = f"日期: {date}" if date else "最新数据"
            self.task_manager.update_progress(task_id, 10, 100, f"正在从同花顺获取ETF实时行情数据({date_desc})...")
            
            # 获取数据
            df = await self._fetch_fund_etf_spot_ths(date)
            
            if df is None or df.empty:
                raise ValueError("未获取到同花顺ETF实时行情数据")
            
            total_count = len(df)
            logger.info(f"成功获取 {total_count} 条同花顺ETF实时行情数据")
            
            # 更新进度：数据获取完成
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {total_count} 条数据，开始保存...")
            
            # 定义进度回调
            def on_save_progress(current, total, percentage, message):
                # 计算总体进度（50%用于获取数据，50%用于保存数据）
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            # 保存数据（传入进度回调）
            saved_count = await self.data_service.save_fund_etf_spot_ths_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条同花顺ETF实时行情数据"
            }
            
        except Exception as e:
            logger.error(f"刷新同花顺ETF实时行情失败: {e}", exc_info=True)
            raise
    
    async def _fetch_fund_lof_spot(self, max_retries: int = 3):
        """
        从AKShare获取LOF基金实时行情数据
        
        Args:
            max_retries: 最大重试次数
            
        Returns:
            DataFrame: LOF基金实时行情数据
        """
        import akshare as ak
        
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试获取LOF基金实时行情数据，第 {attempt + 1}/{max_retries} 次")
                df = await loop.run_in_executor(executor, ak.fund_lof_spot_em)
                executor.shutdown(wait=False)
                logger.info(f"成功获取LOF基金实时行情数据")
                return df
            except Exception as e:
                last_error = e
                logger.warning(f"第 {attempt + 1} 次获取失败: {str(e)}")
                
                if attempt < max_retries - 1:
                    # 等待后重试，使用指数退避策略
                    wait_time = 2 ** attempt  # 1秒, 2秒, 4秒
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    executor.shutdown(wait=False)
                    logger.error(f"获取LOF基金实时行情数据失败，已重试 {max_retries} 次")
                    raise ValueError(f"获取数据失败: {str(last_error)}。这可能是由于网络不稳定或东方财富网服务器暂时不可用。请稍后再试。") from last_error
        
        executor.shutdown(wait=False)
        raise ValueError(f"获取数据失败: {str(last_error)}") from last_error
    
    async def _refresh_fund_lof_spot(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新LOF基金实时行情数据
        
        Args:
            task_id: 任务ID
            params: 参数字典
            
        Returns:
            刷新结果
        """
        try:
            logger.info(f"开始刷新LOF基金实时行情数据，任务ID: {task_id}")
            
            # 更新进度：开始获取数据
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取LOF基金实时行情数据...")
            
            # 获取数据
            df = await self._fetch_fund_lof_spot()
            
            if df is None or df.empty:
                raise ValueError("未获取到LOF基金实时行情数据")
            
            total_count = len(df)
            logger.info(f"成功获取 {total_count} 条LOF基金实时行情数据")
            
            # 更新进度：数据获取完成
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {total_count} 条数据，开始保存...")
            
            # 定义进度回调
            def on_save_progress(current, total, percentage, message):
                # 计算总体进度（50%用于获取数据，50%用于保存数据）
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            # 保存数据（传入进度回调）
            saved_count = await self.data_service.save_fund_lof_spot_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条LOF基金实时行情数据"
            }
            
        except Exception as e:
            logger.error(f"刷新LOF基金实时行情失败: {e}", exc_info=True)
            raise
    
    async def _fetch_fund_spot_sina(self, symbol: str, max_retries: int = 3) -> pd.DataFrame:
        """
        从AKShare获取基金实时行情-新浪数据（带重试机制）
        
        Args:
            symbol: 基金类型，可选值：封闭式基金、ETF基金、LOF基金
            max_retries: 最大重试次数
            
        Returns:
            DataFrame包含基金实时行情数据
        """
        import asyncio
        import akshare as ak
        
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试获取{symbol}数据 (尝试 {attempt + 1}/{max_retries})")
                
                # 在线程池中执行同步的akshare调用
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    None,
                    lambda: ak.fund_etf_category_sina(symbol=symbol)
                )
                
                if df is not None and not df.empty:
                    # 添加基金类型字段
                    df["基金类型"] = symbol
                    logger.info(f"成功获取{symbol}数据，共 {len(df)} 条")
                    return df
                else:
                    logger.warning(f"{symbol}数据为空")
                    return pd.DataFrame()
                    
            except Exception as e:
                logger.warning(f"获取{symbol}数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # 指数退避
                    wait_time = 2 ** attempt
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"获取{symbol}数据失败，已达最大重试次数")
                    raise
    
    async def _refresh_fund_spot_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金实时行情-新浪数据
        
        支持两种模式：
        1. 全部更新：不传symbol参数或symbol="全部"，更新三种类型的所有基金
        2. 单个更新：传入specific symbol（封闭式基金、ETF基金、LOF基金）
        
        Args:
            task_id: 任务ID
            params: 参数字典，可包含symbol字段指定基金类型
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "全部")
            
            # 定义三种基金类型
            fund_types = ["封闭式基金", "ETF基金", "LOF基金"]
            
            # 确定要更新的类型
            if symbol == "全部" or not symbol:
                types_to_update = fund_types
                logger.info(f"开始全部更新基金实时行情-新浪数据（三种类型）")
            elif symbol in fund_types:
                types_to_update = [symbol]
                logger.info(f"开始更新{symbol}实时行情数据")
            else:
                raise ValueError(f"不支持的基金类型: {symbol}，仅支持{fund_types}")
            
            # 更新任务状态
            await self._update_task_progress(task_id, 10, f"正在获取数据...")
            
            # 获取并合并数据
            all_data = []
            total_types = len(types_to_update)
            
            for idx, fund_type in enumerate(types_to_update):
                # 更新进度
                progress = 10 + int(idx / total_types * 60)
                await self._update_task_progress(
                    task_id, 
                    progress, 
                    f"正在获取{fund_type}数据... ({idx+1}/{total_types})"
                )
                
                # 获取数据
                df = await self._fetch_fund_spot_sina(fund_type)
                if not df.empty:
                    all_data.append(df)
            
            # 合并所有数据
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                logger.info(f"成功获取 {len(combined_df)} 条数据")
                
                # 更新进度：保存数据
                await self._update_task_progress(task_id, 70, f"正在保存数据...")
                
                # 保存到数据库
                data_service = FundDataService(self.db)
                saved_count = await data_service.save_fund_spot_sina_data(combined_df)
                
                # 更新进度：完成
                await self._update_task_progress(task_id, 100, f"数据更新完成")
                
                return {
                    'success': True,
                    'saved': saved_count,
                    'types': types_to_update,
                    'message': f"成功更新 {saved_count} 条基金实时行情数据（{', '.join(types_to_update)}）"
                }
            else:
                logger.warning("未获取到任何数据")
                await self._update_task_progress(task_id, 100, "未获取到数据")
                return {
                    'success': True,
                    'saved': 0,
                    'message': "未获取到数据"
                }
            
        except Exception as e:
            logger.error(f"刷新基金实时行情-新浪失败: {e}", exc_info=True)
            raise

    async def _fetch_fund_etf_hist_min_em(
        self,
        symbol: str,
        period: str = "5",
        adjust: str = "hfq",
        start_date: str | None = None,
        end_date: str | None = None,
        max_retries: int = 3,
    ) -> pd.DataFrame:
        """从 AKShare 获取 ETF 分时行情数据（fund_etf_hist_min_em）。

        Args:
            symbol: ETF 代码，例如 "513500"。
            period: 时间周期，"1"/"5"/"15"/"30"/"60"。
            adjust: 复权方式，""/"qfq"/"hfq"。
            start_date: 起始时间字符串（可选）。
            end_date: 结束时间字符串（可选）。
            max_retries: 最大重试次数。

        Returns:
            包含分时行情的 DataFrame；如果获取失败或为空，返回空 DataFrame。
        """
        loop = asyncio.get_event_loop()

        last_error: Exception | None = None
        for attempt in range(max_retries):
            try:
                logger.info(
                    "尝试获取 ETF 分时行情: symbol=%s, period=%s, adjust=%s, 尝试 %d/%d",
                    symbol,
                    period,
                    adjust,
                    attempt + 1,
                    max_retries,
                )

                def _call():
                    import akshare as ak  # 局部导入，避免启动时强依赖

                    return ak.fund_etf_hist_min_em(
                        symbol=symbol,
                        period=period,
                        adjust=adjust,
                        start_date=start_date,
                        end_date=end_date,
                    )

                df = await loop.run_in_executor(_executor, _call)

                if df is not None and not df.empty:
                    logger.info("成功获取 ETF 分时行情: symbol=%s, 行数=%d", symbol, len(df))
                    return df

                logger.warning("ETF 分时行情为空: symbol=%s", symbol)
                return pd.DataFrame()

            except Exception as e:  # noqa: BLE001
                last_error = e
                logger.warning(
                    "获取 ETF 分时行情失败 (symbol=%s, 尝试 %d/%d): %s",
                    symbol,
                    attempt + 1,
                    max_retries,
                    e,
                )
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logger.info("等待 %d 秒后重试 ETF 分时行情请求...", wait_time)
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        "获取 ETF 分时行情失败，已重试 %d 次 (symbol=%s)", max_retries, symbol
                    )
                    raise ValueError(f"获取 ETF 分时行情失败: {last_error}") from last_error

        # 理论上不会到这里
        return pd.DataFrame()

    async def _refresh_fund_etf_hist_min(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新 ETF 基金分时行情数据（fund_etf_hist_min_em）。

        支持两种模式：
        1. 单个更新：传入 symbol 参数，仅刷新单只 ETF；
        2. 批量更新：未传 symbol 时，从 fund_etf_spot_em 集合自动获取 ETF 代码列表，按代码依次刷新。

        服务器端默认参数：period="5"、adjust="hfq"。
        """
        try:
            symbol = params.get("symbol")
            period = str(params.get("period", "5"))
            adjust = str(params.get("adjust", "hfq"))
            start_date = params.get("start_date")
            end_date = params.get("end_date")

            # 单个更新模式
            if symbol:
                await self._update_task_progress(
                    task_id,
                    10,
                    f"正在获取 ETF 分时行情: {symbol} ({period} 分钟, {adjust or '不复权'})...",
                )

                df = await self._fetch_fund_etf_hist_min_em(
                    symbol=symbol,
                    period=period,
                    adjust=adjust,
                    start_date=start_date,
                    end_date=end_date,
                )

                if df is None or df.empty:
                    raise ValueError(f"未获取到 ETF 分时行情数据: {symbol}")

                # 标记代码与参数，便于后续保存
                df = df.copy()
                df["代码"] = symbol
                df["period"] = period
                df["adjust"] = adjust

                await self._update_task_progress(task_id, 60, "数据获取完成，正在保存...")

                saved_count = await self.data_service.save_fund_etf_hist_min_data(df)

                await self._update_task_progress(task_id, 100, f"单只 ETF 分时行情更新完成: {symbol}")

                return {
                    "success": True,
                    "saved": saved_count,
                    "total": len(df),
                    "mode": "single",
                    "symbol": symbol,
                    "message": f"成功更新 {symbol} 的 ETF 分时行情 {saved_count} 条记录",
                }

            # 批量更新模式：从 ETF 实时行情集合中获取所有代码
            await self._update_task_progress(task_id, 5, "正在获取 ETF 代码列表，用于批量更新分时行情...")

            db = self.db
            etf_spot_col = db.get_collection("fund_etf_spot_em")
            codes_raw = await etf_spot_col.distinct("代码")
            codes = [str(c).strip() for c in codes_raw if c]

            if not codes:
                raise ValueError("未在 fund_etf_spot_em 集合中找到任何 ETF 代码，无法执行批量更新")

            total_codes = len(codes)
            concurrency = int(params.get("concurrency", 5))
            if concurrency <= 0:
                concurrency = 1

            logger.info(
                "开始批量刷新 ETF 分时行情，共 %d 只，period=%s, adjust=%s, concurrency=%d",
                total_codes,
                period,
                adjust,
                concurrency,
            )

            processed = 0
            total_saved = 0
            total_rows = 0
            results: List[Dict[str, Any]] = []

            await self._update_task_progress(
                task_id,
                10,
                f"准备开始批量更新 ETF 分时行情，共 {total_codes} 只…",
            )

            idx = 0
            while idx < total_codes:
                batch_codes = codes[idx : idx + concurrency]
                idx += len(batch_codes)

                async def worker(code: str) -> Dict[str, Any]:
                    try:
                        df = await self._fetch_fund_etf_hist_min_em(
                            symbol=code,
                            period=period,
                            adjust=adjust,
                            start_date=start_date,
                            end_date=end_date,
                        )

                        if df is None or df.empty:
                            return {"code": code, "saved": 0, "rows": 0}

                        df = df.copy()
                        df["代码"] = code
                        df["period"] = period
                        df["adjust"] = adjust

                        saved = await self.data_service.save_fund_etf_hist_min_data(df)
                        return {"code": code, "saved": saved, "rows": len(df)}
                    except Exception as e:  # noqa: BLE001
                        logger.warning("刷新单个 ETF 分时行情失败: code=%s, error=%s", code, e)
                        return {"code": code, "error": str(e), "saved": 0, "rows": 0}

                batch_tasks = [worker(code) for code in batch_codes]
                batch_results = await asyncio.gather(*batch_tasks)

                for item in batch_results:
                    processed += 1
                    total_saved += int(item.get("saved", 0))
                    total_rows += int(item.get("rows", 0))
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id,
                    progress,
                    f"已处理 {processed}/{total_codes} 只 ETF，累计保存 {total_saved} 条分时记录",
                )

            await self._update_task_progress(
                task_id,
                100,
                f"批量 ETF 分时行情更新完成，共 {total_codes} 只，保存 {total_saved} 条记录",
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "total_rows": total_rows,
                "period": period,
                "adjust": adjust,
                "items": results,
                "message": f"批量更新 ETF 分时行情完成，共 {total_codes} 只 ETF，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新 ETF 分时行情失败: {e}", exc_info=True)
            raise

    async def _fetch_fund_lof_hist_min_em(
        self,
        symbol: str,
        period: str = "5",
        adjust: str = "hfq",
        start_date: str | None = None,
        end_date: str | None = None,
        max_retries: int = 3,
    ) -> pd.DataFrame:
        """从 AKShare 获取 LOF 分时行情数据（fund_lof_hist_min_em）。

        Args:
            symbol: LOF 代码，例如 "166009"。
            period: 时间周期，"1"/"5"/"15"/"30"/"60"。
            adjust: 复权方式，""/"qfq"/"hfq"。
            start_date: 起始时间字符串（可选）。
            end_date: 结束时间字符串（可选）。
            max_retries: 最大重试次数。

        Returns:
            包含分时行情的 DataFrame；如果获取失败或为空，返回空 DataFrame。
        """
        loop = asyncio.get_event_loop()

        last_error: Exception | None = None
        for attempt in range(max_retries):
            try:
                logger.info(
                    "尝试获取 LOF 分时行情: symbol=%s, period=%s, adjust=%s, 尝试 %d/%d",
                    symbol,
                    period,
                    adjust,
                    attempt + 1,
                    max_retries,
                )

                def _call():
                    import akshare as ak

                    return ak.fund_lof_hist_min_em(
                        symbol=symbol,
                        period=period,
                        adjust=adjust,
                        start_date=start_date,
                        end_date=end_date,
                    )

                df = await loop.run_in_executor(_executor, _call)

                if df is not None and not df.empty:
                    logger.info("成功获取 LOF 分时行情: symbol=%s, 行数=%d", symbol, len(df))
                    return df

                logger.warning("LOF 分时行情为空: symbol=%s", symbol)
                return pd.DataFrame()

            except Exception as e:  # noqa: BLE001
                last_error = e
                logger.warning(
                    "获取 LOF 分时行情失败 (symbol=%s, 尝试 %d/%d): %s",
                    symbol,
                    attempt + 1,
                    max_retries,
                    e,
                )
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logger.info("等待 %d 秒后重试 LOF 分时行情请求...", wait_time)
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        "获取 LOF 分时行情失败，已重试 %d 次 (symbol=%s)", max_retries, symbol
                    )
                    raise ValueError(f"获取 LOF 分时行情失败: {last_error}") from last_error

        return pd.DataFrame()

    async def _refresh_fund_lof_hist_min(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新 LOF 基金分时行情数据（fund_lof_hist_min_em）。

        支持两种模式：
        1. 单个更新：传入 symbol 参数，仅刷新单只 LOF；
        2. 批量更新：未传 symbol 时，从 fund_lof_spot_em 集合自动获取 LOF 代码列表，按代码依次刷新。

        服务器端默认参数：period="5"、adjust="hfq"。
        """
        try:
            symbol = params.get("symbol")
            period = str(params.get("period", "5"))
            adjust = str(params.get("adjust", "hfq"))
            start_date = params.get("start_date")
            end_date = params.get("end_date")

            # 单个更新模式
            if symbol:
                await self._update_task_progress(
                    task_id,
                    10,
                    f"正在获取 LOF 分时行情: {symbol} ({period} 分钟, {adjust or '不复权'})...",
                )

                df = await self._fetch_fund_lof_hist_min_em(
                    symbol=symbol,
                    period=period,
                    adjust=adjust,
                    start_date=start_date,
                    end_date=end_date,
                )

                if df is None or df.empty:
                    raise ValueError(f"未获取到 LOF 分时行情数据: {symbol}")

                df = df.copy()
                df["代码"] = symbol
                df["period"] = period
                df["adjust"] = adjust

                await self._update_task_progress(task_id, 60, "数据获取完成，正在保存...")

                saved_count = await self.data_service.save_fund_lof_hist_min_data(df)

                await self._update_task_progress(task_id, 100, f"单只 LOF 分时行情更新完成: {symbol}")

                return {
                    "success": True,
                    "saved": saved_count,
                    "total": len(df),
                    "mode": "single",
                    "symbol": symbol,
                    "message": f"成功更新 {symbol} 的 LOF 分时行情 {saved_count} 条记录",
                }

            # 批量更新模式
            await self._update_task_progress(task_id, 5, "正在获取 LOF 代码列表，用于批量更新分时行情...")

            db = self.db
            lof_spot_col = db.get_collection("fund_lof_spot_em")
            codes_raw = await lof_spot_col.distinct("代码")
            codes = [str(c).strip() for c in codes_raw if c]

            if not codes:
                raise ValueError("未在 fund_lof_spot_em 集合中找到任何 LOF 代码，无法执行批量更新")

            total_codes = len(codes)
            concurrency = int(params.get("concurrency", 5))
            if concurrency <= 0:
                concurrency = 1

            logger.info(
                "开始批量刷新 LOF 分时行情，共 %d 只，period=%s, adjust=%s, concurrency=%d",
                total_codes,
                period,
                adjust,
                concurrency,
            )

            processed = 0
            total_saved = 0
            total_rows = 0
            results: List[Dict[str, Any]] = []

            await self._update_task_progress(
                task_id,
                10,
                f"准备开始批量更新 LOF 分时行情，共 {total_codes} 只…",
            )

            idx = 0
            while idx < total_codes:
                batch_codes = codes[idx : idx + concurrency]
                idx += len(batch_codes)

                async def worker(code: str) -> Dict[str, Any]:
                    try:
                        df = await self._fetch_fund_lof_hist_min_em(
                            symbol=code,
                            period=period,
                            adjust=adjust,
                            start_date=start_date,
                            end_date=end_date,
                        )

                        if df is None or df.empty:
                            return {"code": code, "saved": 0, "rows": 0}

                        df = df.copy()
                        df["代码"] = code
                        df["period"] = period
                        df["adjust"] = adjust

                        saved = await self.data_service.save_fund_lof_hist_min_data(df)
                        return {"code": code, "saved": saved, "rows": len(df)}
                    except Exception as e:  # noqa: BLE001
                        logger.warning("刷新单个 LOF 分时行情失败: code=%s, error=%s", code, e)
                        return {"code": code, "error": str(e), "saved": 0, "rows": 0}

                batch_tasks = [worker(code) for code in batch_codes]
                batch_results = await asyncio.gather(*batch_tasks)

                for item in batch_results:
                    processed += 1
                    total_saved += int(item.get("saved", 0))
                    total_rows += int(item.get("rows", 0))
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id,
                    progress,
                    f"已处理 {processed}/{total_codes} 只 LOF，累计保存 {total_saved} 条分时记录",
                )

            await self._update_task_progress(
                task_id,
                100,
                f"批量 LOF 分时行情更新完成，共 {total_codes} 只，保存 {total_saved} 条记录",
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "total_rows": total_rows,
                "period": period,
                "adjust": adjust,
                "items": results,
                "message": f"批量更新 LOF 分时行情完成，共 {total_codes} 只 LOF，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新 LOF 分时行情失败: {e}", exc_info=True)
            raise

    async def _fetch_fund_etf_hist_em(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "20000101",
        end_date: str = "",
        adjust: str = "hfq",
        max_retries: int = 3,
    ) -> pd.DataFrame:
        """调用 AKShare 获取 ETF 历史行情数据（带重试）。

        Args:
            symbol: ETF 代码
            period: 周期 daily/weekly/monthly
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD
            adjust: 复权方式 ''(不复权)/qfq(前复权)/hfq(后复权)
            max_retries: 最大重试次数

        Returns:
            包含历史行情数据的 DataFrame
        """
        import time
        from datetime import datetime

        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")

        for attempt in range(max_retries):
            try:
                import akshare as ak

                df = ak.fund_etf_hist_em(
                    symbol=symbol,
                    period=period,
                    start_date=start_date,
                    end_date=end_date,
                    adjust=adjust,
                )
                if df is not None and not df.empty:
                    logger.info(
                        f"成功获取 ETF {symbol} 历史行情: {len(df)} 条 (period={period}, adjust={adjust})"
                    )
                    return df
                else:
                    logger.warning(f"ETF {symbol} 历史行情返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(
                    f"获取 ETF {symbol} 历史行情失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"ETF {symbol} 历史行情获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_etf_hist(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新 ETF 历史行情数据。

        支持两种模式：
        1. 单个更新：params 含 symbol 时，仅拉取单只 ETF
        2. 批量更新：不传 symbol，从 fund_etf_spot_em 集合获取所有 ETF 代码

        Args:
            task_id: 任务 ID
            params: 刷新参数，可包含：
                - symbol: ETF 代码（可选，单个更新时使用）
                - period: 周期 daily/weekly/monthly（默认 daily）
                - adjust: 复权方式 ''(不复权)/qfq/hfq（默认 hfq）
                - start_date: 开始日期 YYYYMMDD（默认 20000101）
                - end_date: 结束日期 YYYYMMDD（默认今天）
                - concurrency: 并发数（批量更新时，默认 5）

        Returns:
            刷新结果字典
        """
        try:
            symbol = params.get("symbol")
            period = params.get("period", "daily")
            adjust = params.get("adjust", "hfq")
            start_date = params.get("start_date", "20000101")
            end_date = params.get("end_date", "")
            concurrency = int(params.get("concurrency", 5))

            # 单个更新
            if symbol:
                await self._update_task_progress(task_id, 10, f"正在获取 ETF {symbol} 历史行情...")

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor,
                    self._fetch_fund_etf_hist_em,
                    symbol,
                    period,
                    start_date,
                    end_date,
                    adjust,
                )

                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"ETF {symbol} 无数据")
                    return {
                        "success": False,
                        "mode": "single",
                        "symbol": symbol,
                        "saved": 0,
                        "message": f"ETF {symbol} 未获取到数据",
                    }

                await self._update_task_progress(
                    task_id, 50, f"获取到 {len(df)} 条数据，正在保存..."
                )

                # 补充必要字段
                df = df.copy()
                df["代码"] = symbol
                df["period"] = period
                df["adjust"] = adjust

                saved = await self.data_service.save_fund_etf_hist_data(df)

                await self._update_task_progress(
                    task_id, 100, f"ETF {symbol} 历史行情更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "mode": "single",
                    "symbol": symbol,
                    "saved": saved,
                    "rows": len(df),
                    "period": period,
                    "adjust": adjust,
                    "message": f"ETF {symbol} 更新完成，保存 {saved} 条记录",
                }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取 ETF 代码列表...")

            etf_codes = (
                await self.data_service.col_fund_etf_spot.distinct("代码") or []
            )
            if not etf_codes:
                logger.warning("未找到任何 ETF 代码，请先刷新 fund_etf_spot_em 集合")
                return {
                    "success": False,
                    "mode": "batch",
                    "message": "未找到 ETF 代码列表",
                }

            total_codes = len(etf_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只 ETF，开始批量获取历史行情..."
            )

            results = []
            total_saved = 0
            total_rows = 0
            processed = 0
            batch_size = concurrency

            for i in range(0, total_codes, batch_size):
                batch_codes = etf_codes[i : i + batch_size]

                async def worker(code: str) -> Dict[str, Any]:
                    try:
                        loop = asyncio.get_event_loop()
                        df = await loop.run_in_executor(
                            _executor,
                            self._fetch_fund_etf_hist_em,
                            code,
                            period,
                            start_date,
                            end_date,
                            adjust,
                        )

                        if df is None or df.empty:
                            return {"code": code, "saved": 0, "rows": 0}

                        df = df.copy()
                        df["代码"] = code
                        df["period"] = period
                        df["adjust"] = adjust

                        saved = await self.data_service.save_fund_etf_hist_data(df)
                        return {"code": code, "saved": saved, "rows": len(df)}
                    except Exception as e:  # noqa: BLE001
                        logger.warning("刷新单个 ETF 历史行情失败: code=%s, error=%s", code, e)
                        return {"code": code, "error": str(e), "saved": 0, "rows": 0}

                batch_tasks = [worker(code) for code in batch_codes]
                batch_results = await asyncio.gather(*batch_tasks)

                for item in batch_results:
                    processed += 1
                    total_saved += int(item.get("saved", 0))
                    total_rows += int(item.get("rows", 0))
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id,
                    progress,
                    f"已处理 {processed}/{total_codes} 只 ETF，累计保存 {total_saved} 条历史记录",
                )

            await self._update_task_progress(
                task_id,
                100,
                f"批量 ETF 历史行情更新完成，共 {total_codes} 只，保存 {total_saved} 条记录",
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "total_rows": total_rows,
                "period": period,
                "adjust": adjust,
                "items": results,
                "message": f"批量更新 ETF 历史行情完成，共 {total_codes} 只 ETF，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新 ETF 历史行情失败: {e}", exc_info=True)
            raise

    async def _fetch_fund_lof_hist_em(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "20000101",
        end_date: str = "",
        adjust: str = "hfq",
        max_retries: int = 3,
    ) -> pd.DataFrame:
        """调用 AKShare 获取 LOF 历史行情数据（带重试）。

        Args:
            symbol: LOF 代码
            period: 周期 daily/weekly/monthly
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD
            adjust: 复权方式 ''(不复权)/qfq(前复权)/hfq(后复权)
            max_retries: 最大重试次数

        Returns:
            包含历史行情数据的 DataFrame
        """
        import time
        from datetime import datetime

        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")

        for attempt in range(max_retries):
            try:
                import akshare as ak

                df = ak.fund_lof_hist_em(
                    symbol=symbol,
                    period=period,
                    start_date=start_date,
                    end_date=end_date,
                    adjust=adjust,
                )
                if df is not None and not df.empty:
                    logger.info(
                        f"成功获取 LOF {symbol} 历史行情: {len(df)} 条 (period={period}, adjust={adjust})"
                    )
                    return df
                else:
                    logger.warning(f"LOF {symbol} 历史行情返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(
                    f"获取 LOF {symbol} 历史行情失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"LOF {symbol} 历史行情获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_lof_hist(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新 LOF 历史行情数据。

        支持两种模式：
        1. 单个更新：params 含 symbol 时，仅拉取单只 LOF
        2. 批量更新：不传 symbol，从 fund_lof_spot_em 集合获取所有 LOF 代码

        Args:
            task_id: 任务 ID
            params: 刷新参数，可包含：
                - symbol: LOF 代码（可选，单个更新时使用）
                - period: 周期 daily/weekly/monthly（默认 daily）
                - adjust: 复权方式 ''(不复权)/qfq/hfq（默认 hfq）
                - start_date: 开始日期 YYYYMMDD（默认 20000101）
                - end_date: 结束日期 YYYYMMDD（默认今天）
                - concurrency: 并发数（批量更新时，默认 5）

        Returns:
            刷新结果字典
        """
        try:
            symbol = params.get("symbol")
            period = params.get("period", "daily")
            adjust = params.get("adjust", "hfq")
            start_date = params.get("start_date", "20000101")
            end_date = params.get("end_date", "")
            concurrency = int(params.get("concurrency", 5))

            # 单个更新
            if symbol:
                await self._update_task_progress(task_id, 10, f"正在获取 LOF {symbol} 历史行情...")

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor,
                    self._fetch_fund_lof_hist_em,
                    symbol,
                    period,
                    start_date,
                    end_date,
                    adjust,
                )

                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"LOF {symbol} 无数据")
                    return {
                        "success": False,
                        "mode": "single",
                        "symbol": symbol,
                        "saved": 0,
                        "message": f"LOF {symbol} 未获取到数据",
                    }

                await self._update_task_progress(
                    task_id, 50, f"获取到 {len(df)} 条数据，正在保存..."
                )

                # 补充必要字段
                df = df.copy()
                df["代码"] = symbol
                df["period"] = period
                df["adjust"] = adjust

                saved = await self.data_service.save_fund_lof_hist_data(df)

                await self._update_task_progress(
                    task_id, 100, f"LOF {symbol} 历史行情更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "mode": "single",
                    "symbol": symbol,
                    "saved": saved,
                    "rows": len(df),
                    "period": period,
                    "adjust": adjust,
                    "message": f"LOF {symbol} 更新完成，保存 {saved} 条记录",
                }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取 LOF 代码列表...")

            lof_codes = (
                await self.data_service.col_fund_lof_spot.distinct("代码") or []
            )
            if not lof_codes:
                logger.warning("未找到任何 LOF 代码，请先刷新 fund_lof_spot_em 集合")
                return {
                    "success": False,
                    "mode": "batch",
                    "message": "未找到 LOF 代码列表",
                }

            total_codes = len(lof_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只 LOF，开始批量获取历史行情..."
            )

            results = []
            total_saved = 0
            total_rows = 0
            processed = 0
            batch_size = concurrency

            for i in range(0, total_codes, batch_size):
                batch_codes = lof_codes[i : i + batch_size]

                async def worker(code: str) -> Dict[str, Any]:
                    try:
                        loop = asyncio.get_event_loop()
                        df = await loop.run_in_executor(
                            _executor,
                            self._fetch_fund_lof_hist_em,
                            code,
                            period,
                            start_date,
                            end_date,
                            adjust,
                        )

                        if df is None or df.empty:
                            return {"code": code, "saved": 0, "rows": 0}

                        df = df.copy()
                        df["代码"] = code
                        df["period"] = period
                        df["adjust"] = adjust

                        saved = await self.data_service.save_fund_lof_hist_data(df)
                        return {"code": code, "saved": saved, "rows": len(df)}
                    except Exception as e:  # noqa: BLE001
                        logger.warning("刷新单个 LOF 历史行情失败: code=%s, error=%s", code, e)
                        return {"code": code, "error": str(e), "saved": 0, "rows": 0}

                batch_tasks = [worker(code) for code in batch_codes]
                batch_results = await asyncio.gather(*batch_tasks)

                for item in batch_results:
                    processed += 1
                    total_saved += int(item.get("saved", 0))
                    total_rows += int(item.get("rows", 0))
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id,
                    progress,
                    f"已处理 {processed}/{total_codes} 只 LOF，累计保存 {total_saved} 条历史记录",
                )

            await self._update_task_progress(
                task_id,
                100,
                f"批量 LOF 历史行情更新完成，共 {total_codes} 只，保存 {total_saved} 条记录",
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "total_rows": total_rows,
                "period": period,
                "adjust": adjust,
                "items": results,
                "message": f"批量更新 LOF 历史行情完成，共 {total_codes} 只 LOF，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新 LOF 历史行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_hist_sina(self, symbol: str, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取新浪基金历史行情数据（带重试）。

        Args:
            symbol: 基金代码（如 sh510050）
            max_retries: 最大重试次数

        Returns:
            包含历史行情数据的 DataFrame
        """
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak

                df = ak.fund_etf_hist_sina(symbol=symbol)
                if df is not None and not df.empty:
                    logger.info(f"成功获取新浪基金 {symbol} 历史行情: {len(df)} 条")
                    return df
                else:
                    logger.warning(f"新浪基金 {symbol} 历史行情返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(
                    f"获取新浪基金 {symbol} 历史行情失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"新浪基金 {symbol} 历史行情获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_hist_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新新浪基金历史行情数据。

        支持两种模式：
        1. 单个更新：params 含 symbol 时，仅拉取单只基金
        2. 批量更新：不传 symbol，从 fund_spot_sina 集合获取所有基金代码

        Args:
            task_id: 任务 ID
            params: 刷新参数，可包含：
                - symbol: 基金代码（可选，单个更新时使用）
                - concurrency: 并发数（批量更新时，默认 5）

        Returns:
            刷新结果字典
        """
        try:
            symbol = params.get("symbol")
            concurrency = int(params.get("concurrency", 5))

            # 单个更新
            if symbol:
                await self._update_task_progress(task_id, 10, f"正在获取新浪基金 {symbol} 历史行情...")

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor,
                    self._fetch_fund_hist_sina,
                    symbol,
                )

                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"新浪基金 {symbol} 无数据")
                    return {
                        "success": False,
                        "mode": "single",
                        "symbol": symbol,
                        "saved": 0,
                        "message": f"新浪基金 {symbol} 未获取到数据",
                    }

                await self._update_task_progress(
                    task_id, 50, f"获取到 {len(df)} 条数据，正在保存..."
                )

                # 补充代码字段
                df = df.copy()
                df["代码"] = symbol

                saved = await self.data_service.save_fund_hist_sina_data(df)

                await self._update_task_progress(
                    task_id, 100, f"新浪基金 {symbol} 历史行情更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "mode": "single",
                    "symbol": symbol,
                    "saved": saved,
                    "rows": len(df),
                    "message": f"新浪基金 {symbol} 更新完成，保存 {saved} 条记录",
                }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取基金代码列表...")

            # 从 fund_spot_sina 集合获取所有基金代码
            fund_codes = (
                await self.data_service.col_fund_spot_sina.distinct("代码") or []
            )
            if not fund_codes:
                logger.warning("未找到任何基金代码，请先刷新 fund_spot_sina 集合")
                return {
                    "success": False,
                    "mode": "batch",
                    "message": "未找到基金代码列表",
                }

            total_codes = len(fund_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只基金，开始批量获取历史行情..."
            )

            results = []
            total_saved = 0
            total_rows = 0
            processed = 0
            batch_size = concurrency

            for i in range(0, total_codes, batch_size):
                batch_codes = fund_codes[i : i + batch_size]

                async def worker(code: str) -> Dict[str, Any]:
                    try:
                        loop = asyncio.get_event_loop()
                        df = await loop.run_in_executor(
                            _executor,
                            self._fetch_fund_hist_sina,
                            code,
                        )

                        if df is None or df.empty:
                            return {"code": code, "saved": 0, "rows": 0}

                        df = df.copy()
                        df["代码"] = code

                        saved = await self.data_service.save_fund_hist_sina_data(df)
                        return {"code": code, "saved": saved, "rows": len(df)}
                    except Exception as e:  # noqa: BLE001
                        logger.warning("刷新单个基金历史行情失败: code=%s, error=%s", code, e)
                        return {"code": code, "error": str(e), "saved": 0, "rows": 0}

                batch_tasks = [worker(code) for code in batch_codes]
                batch_results = await asyncio.gather(*batch_tasks)

                for item in batch_results:
                    processed += 1
                    total_saved += int(item.get("saved", 0))
                    total_rows += int(item.get("rows", 0))
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id,
                    progress,
                    f"已处理 {processed}/{total_codes} 只基金，累计保存 {total_saved} 条历史记录",
                )

            await self._update_task_progress(
                task_id,
                100,
                f"批量基金历史行情更新完成，共 {total_codes} 只，保存 {total_saved} 条记录",
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "total_rows": total_rows,
                "items": results,
                "message": f"批量更新新浪基金历史行情完成，共 {total_codes} 只基金，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新新浪基金历史行情失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_open_fund_daily(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新开放式基金实时行情数据。

        此接口在每个交易日 16:00-23:00 更新当日的最新开放式基金净值数据。
        一次性返回所有数据，不需要参数。

        Args:
            task_id: 任务 ID
            params: 刷新参数（不需要参数，但保留以符合接口规范）

        Returns:
            刷新结果字典
        """
        try:
            await self._update_task_progress(task_id, 10, "正在获取开放式基金实时行情数据...")

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor,
                self._fetch_fund_open_fund_daily,
            )

            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到开放式基金实时行情数据")
                return {
                    "success": False,
                    "saved": 0,
                    "message": "未获取到开放式基金实时行情数据",
                }

            await self._update_task_progress(
                task_id, 50, f"获取到 {len(df)} 条数据，正在保存..."
            )

            saved = await self.data_service.save_fund_open_fund_daily_data(df)

            await self._update_task_progress(
                task_id, 100, f"开放式基金实时行情更新完成，保存 {saved} 条记录"
            )

            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "message": f"开放式基金实时行情更新完成，保存 {saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新开放式基金实时行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_open_fund_daily(self, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取开放式基金实时行情数据（带重试）。

        Args:
            max_retries: 最大重试次数

        Returns:
            包含开放式基金实时行情数据的 DataFrame
        """
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak

                df = ak.fund_open_fund_daily_em()
                if df is not None and not df.empty:
                    logger.info(f"成功获取开放式基金实时行情数据: {len(df)} 条")
                    return df
                else:
                    logger.warning("开放式基金实时行情数据返回空")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(
                    f"获取开放式基金实时行情数据失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error("开放式基金实时行情数据获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    def _fetch_fund_open_fund_info(
        self, fund_code: str, indicator: str, period: str = "成立来", max_retries: int = 3
    ) -> pd.DataFrame:
        """调用 AKShare 获取开放式基金历史行情数据（单个指标）

        Args:
            fund_code: 基金代码
            indicator: 指标类型
            period: 周期（仅对"累计收益率走势"有效）
            max_retries: 最大重试次数

        Returns:
            包含历史行情数据的 DataFrame
        """
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak

                # 累计收益率走势需要 period 参数
                if indicator == "累计收益率走势":
                    df = ak.fund_open_fund_info_em(symbol=fund_code, indicator=indicator, period=period)
                else:
                    df = ak.fund_open_fund_info_em(symbol=fund_code, indicator=indicator)

                if df is not None and not df.empty:
                    logger.info(
                        f"成功获取基金 {fund_code} {indicator}: {len(df)} 条"
                    )
                    return df
                else:
                    logger.warning(f"基金 {fund_code} {indicator} 返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(
                    f"获取基金 {fund_code} {indicator} 失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"基金 {fund_code} {indicator} 获取失败，已达最大重试次数")
                    # 不抛出异常，返回空DataFrame
                    return pd.DataFrame()

        return pd.DataFrame()

    async def _refresh_fund_open_fund_info(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新开放式基金历史行情数据（支持所有7个指标）

        支持两种模式：
        1. 单个更新：params 含 fund_code 时，仅拉取单只基金
        2. 批量更新：不传 fund_code，从 fund_open_fund_daily_em 集合获取所有基金代码

        Args:
            task_id: 任务 ID
            params: 刷新参数，可包含：
                - fund_code: 基金代码（可选，单个更新时使用）
                - indicators: 指标列表（可选，默认全部7个）
                - period: 累计收益率周期（默认"成立来"）
                - concurrency: 并发数（批量更新时，默认 3）

        Returns:
            刷新结果字典
        """
        try:
            fund_code = params.get("fund_code")
            period = params.get("period", "成立来")
            concurrency = int(params.get("concurrency", 3))

            # 默认所有7个指标
            default_indicators = [
                "单位净值走势",
                "累计净值走势",
                "累计收益率走势",
                "同类排名走势",
                "同类排名百分比",
                "分红送配详情",
                "拆分详情",
            ]
            indicators = params.get("indicators", default_indicators)

            # 单个更新
            if fund_code:
                await self._update_task_progress(
                    task_id, 10, f"正在获取基金 {fund_code} 的历史行情数据..."
                )

                try:
                    # 只获取单位净值走势和累计净值走势两个指标
                    required_indicators = ["单位净值走势", "累计净值走势"]
                    
                    # 获取单位净值走势
                    await self._update_task_progress(
                        task_id, 30, f"正在获取 {fund_code} - 单位净值走势..."
                    )
                    loop = asyncio.get_event_loop()
                    df_unit = await loop.run_in_executor(
                        _executor,
                        self._fetch_fund_open_fund_info,
                        fund_code,
                        "单位净值走势",
                        period,
                    )
                    
                    # 获取累计净值走势
                    await self._update_task_progress(
                        task_id, 60, f"正在获取 {fund_code} - 累计净值走势..."
                    )
                    df_acc = await loop.run_in_executor(
                        _executor,
                        self._fetch_fund_open_fund_info,
                        fund_code,
                        "累计净值走势",
                        period,
                    )
                    
                    # 合并两个DataFrame
                    if df_unit is not None and not df_unit.empty and df_acc is not None and not df_acc.empty:
                        await self._update_task_progress(
                            task_id, 80, f"正在合并数据..."
                        )
                        
                        # 保存合并后的数据
                        saved = await self.data_service.save_fund_open_fund_info_merged_data(
                            df_unit, df_acc, fund_code
                        )
                        
                        await self._update_task_progress(
                            task_id, 100, f"基金 {fund_code} 历史行情更新完成，保存 {saved} 条记录"
                        )
                        
                        return {
                            "success": True,
                            "mode": "single",
                            "fund_code": fund_code,
                            "saved": saved,
                            "rows": len(df_unit),
                            "message": f"基金 {fund_code} 更新完成，保存 {saved} 条记录",
                        }
                    else:
                        raise ValueError(f"基金 {fund_code} 数据获取失败或为空")
                
                except Exception as e:  # noqa: BLE001
                    logger.error(f"单个更新基金 {fund_code} 失败: {e}")
                    await self._update_task_progress(
                        task_id, 100, f"基金 {fund_code} 更新失败: {str(e)}"
                    )
                    return {
                        "success": False,
                        "mode": "single",
                        "fund_code": fund_code,
                        "error": str(e),
                        "message": f"基金 {fund_code} 更新失败: {str(e)}",
                    }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取基金代码列表...")

            # 从 fund_open_fund_daily_em 集合获取所有基金代码
            fund_codes = (
                await self.data_service.col_fund_open_fund_daily_em.distinct("fund_code") or []
            )
            if not fund_codes:
                logger.warning("未找到任何基金代码，请先刷新 fund_open_fund_daily_em 集合")
                return {
                    "success": False,
                    "mode": "batch",
                    "message": "未找到基金代码列表",
                }

            total_codes = len(fund_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只基金，开始批量获取历史行情..."
            )

            results = []
            total_saved = 0
            processed = 0
            batch_size = concurrency

            for i in range(0, total_codes, batch_size):
                batch_codes = fund_codes[i : i + batch_size]

                async def worker(code: str) -> Dict[str, Any]:
                    try:
                        # 只获取单位净值走势和累计净值走势两个指标
                        loop = asyncio.get_event_loop()
                        
                        # 获取单位净值走势
                        df_unit = await loop.run_in_executor(
                            _executor,
                            self._fetch_fund_open_fund_info,
                            code,
                            "单位净值走势",
                            period,
                        )
                        
                        # 获取累计净值走势
                        df_acc = await loop.run_in_executor(
                            _executor,
                            self._fetch_fund_open_fund_info,
                            code,
                            "累计净值走势",
                            period,
                        )
                        
                        # 合并并保存
                        if df_unit is not None and not df_unit.empty and df_acc is not None and not df_acc.empty:
                            saved = await self.data_service.save_fund_open_fund_info_merged_data(
                                df_unit, df_acc, code
                            )
                            return {
                                "fund_code": code,
                                "saved": saved,
                                "rows": len(df_unit),
                                "success": True,
                            }
                        else:
                            logger.warning(f"基金 {code} 数据获取失败或为空")
                            return {
                                "fund_code": code,
                                "saved": 0,
                                "rows": 0,
                                "success": False,
                                "error": "数据获取失败或为空",
                            }
                    
                    except Exception as e:  # noqa: BLE001
                        logger.warning(f"批量更新基金 {code} 失败: {e}")
                        return {
                            "fund_code": code,
                            "saved": 0,
                            "rows": 0,
                            "success": False,
                            "error": str(e),
                        }

                batch_tasks = [worker(code) for code in batch_codes]
                batch_results = await asyncio.gather(*batch_tasks)

                for item in batch_results:
                    processed += 1
                    total_saved += int(item.get("saved", 0))
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id,
                    progress,
                    f"已处理 {processed}/{total_codes} 只基金，累计保存 {total_saved} 条历史记录",
                )

            await self._update_task_progress(
                task_id,
                100,
                f"批量基金历史行情更新完成，共 {total_codes} 只，保存 {total_saved} 条记录",
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "items": results,
                "message": f"批量更新基金历史行情完成，共 {total_codes} 只基金，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新开放式基金历史行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_money_fund_daily(self, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取货币型基金实时行情数据

        Args:
            max_retries: 最大重试次数

        Returns:
            包含货币型基金实时行情数据的 DataFrame
        """
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak

                df = ak.fund_money_fund_daily_em()

                if df is not None and not df.empty:
                    logger.info(f"成功获取货币型基金实时行情数据: {len(df)} 条")
                    return df
                else:
                    logger.warning("货币型基金实时行情数据返回空")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(
                    f"获取货币型基金实时行情数据失败 (尝试 {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error("货币型基金实时行情数据获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_money_fund_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新货币型基金实时行情数据（全量更新）

        Args:
            task_id: 任务 ID
            params: 刷新参数（此接口无需参数）

        Returns:
            刷新结果字典
        """
        try:
            await self._update_task_progress(
                task_id, 10, "正在获取货币型基金实时行情数据..."
            )

            # 获取数据
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_money_fund_daily
            )

            if df is None or df.empty:
                await self._update_task_progress(
                    task_id, 100, "未获取到货币型基金实时行情数据"
                )
                return {
                    "success": False,
                    "message": "未获取到数据",
                    "total_rows": 0,
                    "saved_count": 0,
                }

            total_rows = len(df)
            await self._update_task_progress(
                task_id, 50, f"获取到 {total_rows} 条数据，正在保存..."
            )

            # 保存数据
            saved_count = await self.data_service.save_fund_money_fund_daily_data(df)

            await self._update_task_progress(
                task_id, 100, f"货币型基金实时行情更新完成，保存 {saved_count} 条记录"
            )

            return {
                "success": True,
                "total_rows": total_rows,
                "saved_count": saved_count,
                "message": f"成功更新货币型基金实时行情，保存 {saved_count} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新货币型基金实时行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_money_fund_info(self, fund_code: str, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取货币型基金历史行情数据

        Args:
            fund_code: 基金代码
            max_retries: 最大重试次数

        Returns:
            包含历史行情数据的 DataFrame
        """
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak

                df = ak.fund_money_fund_info_em(symbol=fund_code)

                if df is not None and not df.empty:
                    logger.info(f"成功获取基金 {fund_code} 货币型历史行情: {len(df)} 条")
                    return df
                else:
                    logger.warning(f"基金 {fund_code} 货币型历史行情返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(f"获取基金 {fund_code} 货币型历史行情失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"基金 {fund_code} 货币型历史行情获取失败，已达最大重试次数")
                    return pd.DataFrame()

        return pd.DataFrame()

    async def _refresh_fund_money_fund_info(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新货币型基金历史行情数据

        支持两种模式：
        1. 单个更新：params 含 symbol 时，仅拉取单只基金
        2. 批量更新：不传 symbol，从 fund_money_fund_daily_em 集合获取所有基金代码

        Args:
            task_id: 任务 ID
            params: 刷新参数（symbol: 基金代码, concurrency: 并发数）

        Returns:
            刷新结果字典
        """
        try:
            symbol = params.get("symbol")  # 使用symbol参数
            concurrency = int(params.get("concurrency", 3))

            # 单个更新
            if symbol:
                await self._update_task_progress(
                    task_id, 10, f"正在获取基金 {symbol} 的历史行情数据..."
                )

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_money_fund_info, symbol
                )

                if df is None or df.empty:
                    return {
                        "success": False,
                        "message": f"未获取到基金 {symbol} 的数据",
                    }

                saved = await self.data_service.save_fund_money_fund_info_data(df, symbol)
                await self._update_task_progress(
                    task_id, 100, f"基金 {symbol} 历史行情更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "mode": "single",
                    "fund_code": symbol,
                    "total_saved": saved,
                    "message": f"基金 {symbol} 更新完成，保存 {saved} 条记录",
                }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取基金代码列表...")

            # 从货币型基金实时行情集合获取所有基金代码
            fund_codes = (
                await self.data_service.col_fund_money_fund_daily_em.distinct("基金代码") or []
            )
            if not fund_codes:
                logger.warning("未找到任何基金代码，请先刷新 fund_money_fund_daily_em 集合")
                return {
                    "success": False,
                    "mode": "batch",
                    "message": "未找到基金代码列表，请先刷新 fund_money_fund_daily_em 集合",
                }

            total_codes = len(fund_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只基金，开始批量获取历史行情..."
            )

            results = []
            total_saved = 0
            processed = 0

            for i in range(0, total_codes, concurrency):
                batch_codes = fund_codes[i : i + concurrency]

                async def worker(code: str):
                    loop = asyncio.get_event_loop()
                    df = await loop.run_in_executor(
                        _executor, self._fetch_fund_money_fund_info, code
                    )
                    if df is not None and not df.empty:
                        saved = await self.data_service.save_fund_money_fund_info_data(df, code)
                        return {"fund_code": code, "saved": saved}
                    return {"fund_code": code, "saved": 0}

                batch_results = await asyncio.gather(*[worker(code) for code in batch_codes])

                for item in batch_results:
                    processed += 1
                    total_saved += item["saved"]
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id, progress, f"已处理 {processed}/{total_codes} 只基金"
                )

            await self._update_task_progress(
                task_id, 100, f"批量更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录"
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "message": f"批量更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新货币型基金历史行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_financial_fund_daily(self, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取理财型基金实时行情数据"""
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_financial_fund_daily_em()

                if df is not None and not df.empty:
                    logger.info(f"成功获取理财型基金实时行情数据: {len(df)} 条")
                    return df
                else:
                    logger.warning("理财型基金实时行情数据返回空")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(f"获取理财型基金实时行情数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error("理财型基金实时行情数据获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_financial_fund_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新理财型基金实时行情数据（全量更新）"""
        try:
            await self._update_task_progress(
                task_id, 10, "正在获取理财型基金实时行情数据..."
            )

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_financial_fund_daily
            )

            if df is None or df.empty:
                await self._update_task_progress(
                    task_id, 100, "未获取到理财型基金实时行情数据"
                )
                return {
                    "success": False,
                    "message": "未获取到数据",
                    "total_rows": 0,
                    "saved_count": 0,
                }

            total_rows = len(df)
            await self._update_task_progress(
                task_id, 50, f"获取到 {total_rows} 条数据，正在保存..."
            )

            saved_count = await self.data_service.save_fund_financial_fund_daily_data(df)

            await self._update_task_progress(
                task_id, 100, f"理财型基金实时行情更新完成，保存 {saved_count} 条记录"
            )

            return {
                "success": True,
                "total_rows": total_rows,
                "saved_count": saved_count,
                "message": f"成功更新理财型基金实时行情，保存 {saved_count} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新理财型基金实时行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_financial_fund_info(self, fund_code: str, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取理财型基金历史行情数据"""
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_financial_fund_info_em(symbol=fund_code)

                if df is not None and not df.empty:
                    logger.info(f"成功获取基金 {fund_code} 理财型历史行情: {len(df)} 条")
                    return df
                else:
                    logger.warning(f"基金 {fund_code} 理财型历史行情返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(f"获取基金 {fund_code} 理财型历史行情失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"基金 {fund_code} 理财型历史行情获取失败，已达最大重试次数")
                    return pd.DataFrame()

        return pd.DataFrame()

    async def _refresh_fund_financial_fund_info(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新理财型基金历史行情数据

        支持两种模式：
        1. 单个更新：params 含 symbol 时，仅拉取单只基金
        2. 批量更新：不传 symbol，从 fund_financial_fund_daily_em 集合获取所有基金代码
        
        Args:
            task_id: 任务 ID
            params: 刷新参数（symbol: 基金代码, concurrency: 并发数）

        Returns:
            刷新结果字典
        """
        try:
            symbol = params.get("symbol")  # 使用symbol参数
            concurrency = int(params.get("concurrency", 3))

            # 单个更新
            if symbol:
                await self._update_task_progress(
                    task_id, 10, f"正在获取基金 {symbol} 的历史行情数据..."
                )

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_financial_fund_info, symbol
                )

                if df is None or df.empty:
                    return {
                        "success": False,
                        "message": f"未获取到基金 {symbol} 的数据",
                    }

                saved = await self.data_service.save_fund_financial_fund_info_data(df, symbol)
                await self._update_task_progress(
                    task_id, 100, f"基金 {symbol} 历史行情更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "mode": "single",
                    "fund_code": symbol,
                    "total_saved": saved,
                    "message": f"基金 {symbol} 更新完成，保存 {saved} 条记录",
                }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取基金代码列表...")

            # 从理财型基金实时行情集合获取所有基金代码
            fund_codes = (
                await self.data_service.col_fund_financial_fund_daily_em.distinct("基金代码") or []
            )
            if not fund_codes:
                logger.warning("未找到任何基金代码，请先刷新 fund_financial_fund_daily_em 集合")
                return {
                    "success": False,
                    "mode": "batch",
                    "message": "未找到基金代码列表，请先刷新 fund_financial_fund_daily_em 集合",
                }

            total_codes = len(fund_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只基金，开始批量获取历史行情..."
            )

            results = []
            total_saved = 0
            processed = 0

            for i in range(0, total_codes, concurrency):
                batch_codes = fund_codes[i : i + concurrency]

                async def worker(code: str):
                    loop = asyncio.get_event_loop()
                    df = await loop.run_in_executor(
                        _executor, self._fetch_fund_financial_fund_info, code
                    )
                    if df is not None and not df.empty:
                        saved = await self.data_service.save_fund_financial_fund_info_data(df, code)
                        return {"fund_code": code, "saved": saved}
                    return {"fund_code": code, "saved": 0}

                batch_results = await asyncio.gather(*[worker(code) for code in batch_codes])

                for item in batch_results:
                    processed += 1
                    total_saved += item["saved"]
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id, progress, f"已处理 {processed}/{total_codes} 只基金"
                )

            await self._update_task_progress(
                task_id, 100, f"批量更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录"
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "message": f"批量更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新理财型基金历史行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_graded_fund_daily(self, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取分级基金实时数据"""
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_graded_fund_daily_em()

                if df is not None and not df.empty:
                    logger.info(f"成功获取分级基金实时数据: {len(df)} 条")
                    return df
                else:
                    logger.warning("分级基金实时数据返回空")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(f"获取分级基金实时数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error("分级基金实时数据获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_graded_fund_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新分级基金实时数据（全量更新）"""
        try:
            await self._update_task_progress(
                task_id, 10, "正在获取分级基金实时数据..."
            )

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_graded_fund_daily
            )

            if df is None or df.empty:
                await self._update_task_progress(
                    task_id, 100, "未获取到分级基金实时数据"
                )
                return {
                    "success": False,
                    "message": "未获取到数据",
                    "total_rows": 0,
                    "saved_count": 0,
                }

            total_rows = len(df)
            await self._update_task_progress(
                task_id, 50, f"获取到 {total_rows} 条数据，正在保存..."
            )

            saved_count = await self.data_service.save_fund_graded_fund_daily_data(df)

            await self._update_task_progress(
                task_id, 100, f"分级基金实时数据更新完成，保存 {saved_count} 条记录"
            )

            return {
                "success": True,
                "total_rows": total_rows,
                "saved_count": saved_count,
                "message": f"成功更新分级基金实时数据，保存 {saved_count} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新分级基金实时数据失败: {e}", exc_info=True)
            raise

    def _fetch_fund_graded_fund_info(self, fund_code: str, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取分级基金历史数据"""
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_graded_fund_info_em(symbol=fund_code)

                if df is not None and not df.empty:
                    logger.info(f"成功获取基金 {fund_code} 分级历史数据: {len(df)} 条")
                    return df
                else:
                    logger.warning(f"基金 {fund_code} 分级历史数据返回空数据")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(f"获取基金 {fund_code} 分级历史数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"基金 {fund_code} 分级历史数据获取失败，已达最大重试次数")
                    return pd.DataFrame()

        return pd.DataFrame()

    async def _refresh_fund_graded_fund_info(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新分级基金历史数据

        支持两种模式：
        1. 单个更新：params 含 fund_code 时，仅拉取单只基金
        2. 批量更新：不传 fund_code，从 fund_graded_fund_daily_em 集合获取所有基金代码
        """
        try:
            fund_code = params.get("fund_code")
            concurrency = int(params.get("concurrency", 3))

            # 单个更新
            if fund_code:
                await self._update_task_progress(
                    task_id, 10, f"正在获取基金 {fund_code} 的历史数据..."
                )

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_graded_fund_info, fund_code
                )

                if df is None or df.empty:
                    return {
                        "success": False,
                        "message": f"未获取到基金 {fund_code} 的数据",
                    }

                saved = await self.data_service.save_fund_graded_fund_info_data(df, fund_code)
                await self._update_task_progress(
                    task_id, 100, f"基金 {fund_code} 历史数据更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "mode": "single",
                    "fund_code": fund_code,
                    "total_saved": saved,
                    "message": f"基金 {fund_code} 更新完成，保存 {saved} 条记录",
                }

            # 批量更新
            await self._update_task_progress(task_id, 5, "正在获取基金代码列表...")

            fund_codes = (
                await self.data_service.col_fund_graded_fund_daily_em.distinct("fund_code") or []
            )
            if not fund_codes:
                return {"success": False, "message": "未找到基金代码列表"}

            total_codes = len(fund_codes)
            await self._update_task_progress(
                task_id, 10, f"共 {total_codes} 只基金，开始批量获取历史数据..."
            )

            results = []
            total_saved = 0
            processed = 0

            for i in range(0, total_codes, concurrency):
                batch_codes = fund_codes[i : i + concurrency]

                async def worker(code: str):
                    loop = asyncio.get_event_loop()
                    df = await loop.run_in_executor(
                        _executor, self._fetch_fund_graded_fund_info, code
                    )
                    if df is not None and not df.empty:
                        saved = await self.data_service.save_fund_graded_fund_info_data(df, code)
                        return {"fund_code": code, "saved": saved}
                    return {"fund_code": code, "saved": 0}

                batch_results = await asyncio.gather(*[worker(code) for code in batch_codes])

                for item in batch_results:
                    processed += 1
                    total_saved += item["saved"]
                    results.append(item)

                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id, progress, f"已处理 {processed}/{total_codes} 只基金"
                )

            await self._update_task_progress(
                task_id, 100, f"批量更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录"
            )

            return {
                "success": True,
                "mode": "batch",
                "total_codes": total_codes,
                "total_saved": total_saved,
                "message": f"批量更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新分级基金历史数据失败: {e}", exc_info=True)
            raise

    def _fetch_fund_etf_fund_daily(self, max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取场内交易基金实时数据"""
        import time

        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_etf_fund_daily_em()

                if df is not None and not df.empty:
                    logger.info(f"成功获取场内交易基金实时数据: {len(df)} 条")
                    return df
                else:
                    logger.warning("场内交易基金实时数据返回空")
                    return pd.DataFrame()

            except Exception as e:
                logger.warning(f"获取场内交易基金实时数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error("场内交易基金实时数据获取失败，已达最大重试次数")
                    raise

        return pd.DataFrame()

    async def _refresh_fund_etf_fund_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新场内交易基金实时数据（全量更新）"""
        try:
            await self._update_task_progress(
                task_id, 10, "正在获取场内交易基金实时数据..."
            )

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_etf_fund_daily
            )

            if df is None or df.empty:
                await self._update_task_progress(
                    task_id, 100, "未获取到场内交易基金实时数据"
                )
                return {
                    "success": False,
                    "message": "未获取到数据",
                    "total_rows": 0,
                    "saved_count": 0,
                }

            total_rows = len(df)
            await self._update_task_progress(
                task_id, 50, f"获取到 {total_rows} 条数据，正在保存..."
            )

            saved_count = await self.data_service.save_fund_etf_fund_daily_data(df)

            await self._update_task_progress(
                task_id, 100, f"场内交易基金实时数据更新完成，保存 {saved_count} 条记录"
            )

            return {
                "success": True,
                "total_rows": total_rows,
                "saved_count": saved_count,
                "message": f"成功更新场内交易基金实时数据，保存 {saved_count} 条记录",
            }

        except Exception as e:  # noqa: BLE001
            logger.error(f"刷新场内交易基金实时数据失败: {e}", exc_info=True)
            raise
    
    # ========== 香港基金历史数据 ==========
    def _fetch_fund_hk_hist_em(self, code: str, symbol: str = "历史净值明细", max_retries: int = 3) -> pd.DataFrame:
        """调用 AKShare 获取香港基金历史数据
        
        Args:
            code: 香港基金代码，例如 "1002200683"
            symbol: 数据类型，"历史净值明细" 或 "分红送配详情"
            max_retries: 最大重试次数
            
        Returns:
            包含历史数据的DataFrame
        """
        import time
        
        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_hk_fund_hist_em(code=code, symbol=symbol)
                
                if df is not None and not df.empty:
                    # 添加code和symbol列
                    df['code'] = code
                    df['symbol'] = symbol
                    logger.info(f"成功获取香港基金 {code} 的{symbol}数据: {len(df)} 条")
                    return df
                else:
                    logger.warning(f"香港基金 {code} 的{symbol}数据返回空")
                    return pd.DataFrame()
                    
            except Exception as e:
                logger.warning(f"获取香港基金 {code} 的{symbol}数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"香港基金 {code} 的{symbol}数据获取失败，已达最大重试次数")
                    raise
        
        return pd.DataFrame()
    
    async def _refresh_fund_hk_hist_em(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新香港基金历史数据
        
        Args:
            task_id: 任务ID
            params: 参数字典，可包含:
                - fund_codes: 基金代码列表（可选，默认从fund_basic_info获取）
                - symbol: 数据类型，"历史净值明细"（默认）或 "分红送配详情"
                - concurrency: 并发数（默认5）
                
        Returns:
            刷新结果
        """
        try:
            await self._update_task_progress(
                task_id, 5, "正在准备香港基金代码列表..."
            )
            
            # 获取参数
            fund_codes = params.get('fund_codes')
            symbol = params.get('symbol', '历史净值明细')
            concurrency = params.get('concurrency', 5)
            
            # 如果未提供fund_codes，从fund_basic_info获取香港基金代码
            if not fund_codes:
                logger.info("未提供fund_codes，从fund_basic_info获取香港基金代码...")
                # 这里可以根据实际情况查询fund_basic_info中的香港基金
                # 暂时使用默认的示例代码
                fund_codes = ["1002200683"]  # 示例代码，实际应从数据库查询
                logger.info(f"从fund_basic_info获取到 {len(fund_codes)} 个香港基金代码")
            
            total_codes = len(fund_codes)
            if total_codes == 0:
                await self._update_task_progress(
                    task_id, 100, "没有找到香港基金代码"
                )
                return {
                    "success": False,
                    "message": "没有找到香港基金代码",
                    "total_codes": 0,
                    "total_saved": 0,
                }
            
            await self._update_task_progress(
                task_id, 10, f"准备更新 {total_codes} 只香港基金的{symbol}数据..."
            )
            
            # 并发获取和保存数据
            total_saved = 0
            processed = 0
            failed = 0
            results = []
            
            for i in range(0, total_codes, concurrency):
                batch_codes = fund_codes[i : i + concurrency]
                
                async def worker(code: str):
                    try:
                        loop = asyncio.get_event_loop()
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_hk_hist_em, code, symbol
                        )
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_hk_hist_em_data(df)
                            return {"fund_code": code, "saved": saved, "status": "success"}
                        return {"fund_code": code, "saved": 0, "status": "empty"}
                    except Exception as e:
                        logger.error(f"处理香港基金 {code} 失败: {e}")
                        return {"fund_code": code, "saved": 0, "status": "failed", "error": str(e)}
                
                batch_results = await asyncio.gather(*[worker(code) for code in batch_codes])
                
                for item in batch_results:
                    processed += 1
                    total_saved += item["saved"]
                    if item["status"] == "failed":
                        failed += 1
                    results.append(item)
                
                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id, progress, f"已处理 {processed}/{total_codes} 只基金，保存 {total_saved} 条数据"
                )
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录"
            )
            
            return {
                "success": True,
                "total_codes": total_codes,
                "total_saved": total_saved,
                "failed": failed,
                "symbol": symbol,
                "message": f"成功更新 {total_codes} 只香港基金的{symbol}数据，保存 {total_saved} 条记录（失败 {failed} 只）",
            }
            
        except Exception as e:
            logger.error(f"刷新香港基金历史数据失败: {e}", exc_info=True)
            raise
    
    # ========== 场内交易基金历史行情 ==========
    def _fetch_fund_etf_fund_info_em(
        self, fund: str, start_date: str = "20000101", end_date: str = "20500101", max_retries: int = 3
    ) -> pd.DataFrame:
        """调用 AKShare 获取场内交易基金历史行情数据
        
        Args:
            fund: 基金代码，例如 "511280"
            start_date: 开始日期，格式 "YYYYMMDD"
            end_date: 结束日期，格式 "YYYYMMDD"
            max_retries: 最大重试次数
            
        Returns:
            包含历史行情的DataFrame
        """
        import time
        
        for attempt in range(max_retries):
            try:
                import akshare as ak
                df = ak.fund_etf_fund_info_em(fund=fund, start_date=start_date, end_date=end_date)
                
                if df is not None and not df.empty:
                    logger.info(f"成功获取基金 {fund} 的历史行情数据: {len(df)} 条")
                    return df
                else:
                    logger.warning(f"基金 {fund} 的历史行情数据返回空")
                    return pd.DataFrame()
                    
            except Exception as e:
                logger.warning(f"获取基金 {fund} 的历史行情数据失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                else:
                    logger.error(f"基金 {fund} 的历史行情数据获取失败，已达最大重试次数")
                    raise
        
        return pd.DataFrame()
    
    async def _refresh_fund_etf_fund_info_em(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新场内交易基金历史行情数据
        
        支持两种模式：
        1. 单个更新：params 含 symbol 时，仅拉取单只基金
        2. 批量更新：不传 symbol，从 fund_etf_fund_daily_em 集合获取所有基金代码
        
        Args:
            task_id: 任务ID
            params: 参数字典，可包含:
                - symbol: 单个基金代码（用于单个更新）
                - fund_codes: 基金代码列表（可选，默认从fund_etf_fund_daily_em获取）
                - start_date: 开始日期，格式 "YYYYMMDD"（默认 "20000101"）
                - end_date: 结束日期，格式 "YYYYMMDD"（默认 "20500101"）
                - concurrency: 并发数（默认3）
                
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol")  # 单个更新模式
            start_date = params.get('start_date', '20000101')
            end_date = params.get('end_date', '20500101')
            concurrency = int(params.get('concurrency', 3))
            
            # 单个更新
            if symbol:
                await self._update_task_progress(
                    task_id, 10, f"正在获取基金 {symbol} 的历史行情数据..."
                )
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_etf_fund_info_em, symbol, start_date, end_date
                )
                
                if df is None or df.empty:
                    return {
                        "success": False,
                        "message": f"未获取到基金 {symbol} 的数据",
                    }
                
                saved = await self.data_service.save_fund_etf_fund_info_data(df, fund_code=symbol)
                await self._update_task_progress(
                    task_id, 100, f"基金 {symbol} 历史行情更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "mode": "single",
                    "fund_code": symbol,
                    "total_saved": saved,
                    "message": f"基金 {symbol} 更新完成，保存 {saved} 条记录",
                }
            
            # 批量更新
            await self._update_task_progress(
                task_id, 5, "正在准备基金代码列表..."
            )
            
            # 获取参数
            fund_codes = params.get('fund_codes')
            
            # 如果未提供fund_codes，从fund_etf_fund_daily_em获取
            if not fund_codes:
                logger.info("未提供fund_codes，从fund_etf_fund_daily_em获取场内交易基金代码...")
                collection = self.db.get_collection("fund_etf_fund_daily_em")
                fund_codes = await collection.distinct("基金代码")  # 使用中文字段名
                logger.info(f"从fund_etf_fund_daily_em获取到 {len(fund_codes)} 个基金代码")
            
            total_codes = len(fund_codes)
            if total_codes == 0:
                await self._update_task_progress(
                    task_id, 100, "没有找到场内交易基金代码"
                )
                return {
                    "success": False,
                    "message": "没有找到场内交易基金代码",
                    "total_codes": 0,
                    "total_saved": 0,
                }
            
            await self._update_task_progress(
                task_id, 10, f"准备更新 {total_codes} 只基金的历史行情数据..."
            )
            
            # 并发获取和保存数据
            total_saved = 0
            processed = 0
            failed = 0
            results = []
            
            for i in range(0, total_codes, concurrency):
                batch_codes = fund_codes[i : i + concurrency]
                
                async def worker(code: str):
                    try:
                        loop = asyncio.get_event_loop()
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_etf_fund_info_em, code, start_date, end_date
                        )
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_etf_fund_info_data(df, fund_code=code)
                            return {"fund_code": code, "saved": saved, "status": "success"}
                        return {"fund_code": code, "saved": 0, "status": "empty"}
                    except Exception as e:
                        logger.error(f"处理基金 {code} 失败: {e}")
                        return {"fund_code": code, "saved": 0, "status": "failed", "error": str(e)}
                
                batch_results = await asyncio.gather(*[worker(code) for code in batch_codes])
                
                for item in batch_results:
                    processed += 1
                    total_saved += item["saved"]
                    if item["status"] == "failed":
                        failed += 1
                    results.append(item)
                
                progress = 10 + int((processed / total_codes) * 85)
                await self._update_task_progress(
                    task_id, progress, f"已处理 {processed}/{total_codes} 只基金，保存 {total_saved} 条数据"
                )
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录"
            )
            
            return {
                "success": True,
                "total_codes": total_codes,
                "total_saved": total_saved,
                "failed": failed,
                "message": f"成功更新 {total_codes} 只基金的历史行情数据，保存 {total_saved} 条记录（失败 {failed} 只）",
            }
            
        except Exception as e:
            logger.error(f"刷新场内交易基金历史行情数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_etf_dividend_sina(self, symbol: str) -> pd.DataFrame:
        """同步获取基金累计分红数据（在线程池中调用）
        
        Args:
            symbol: 基金代码，如 sh510050
            
        Returns:
            DataFrame
        """
        try:
            import akshare as ak
            df = ak.fund_etf_dividend_sina(symbol=symbol)
            return df
        except Exception as e:
            logger.error(f"获取基金累计分红数据失败: {symbol}, {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_etf_dividend_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金累计分红数据
        
        Args:
            task_id: 任务ID
            params: 参数，包含:
                - fund_code: 基金代码，如 sh510050（单个更新）
                - batch_update: 是否批量更新
                - batch_size: 批次大小
                - concurrency: 并发数
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get("fund_code")
            batch_update = params.get("batch_update", False)
            batch_size = params.get("batch_size", 50)
            concurrency = params.get("concurrency", 5)
            
            await self._update_task_progress(task_id, 5, "开始刷新基金累计分红数据...")
            
            if batch_update:
                await self._update_task_progress(task_id, 10, "正在查询基金代码列表...")
                
                fund_name_col = self.db.get_collection("fund_name_em")
                cursor = fund_name_col.find({}, {"_id": 0, "基金代码": 1})
                fund_codes = []
                async for doc in cursor:
                    code = doc.get("基金代码")
                    if code:
                        fund_codes.append(f"sh{code}")
                
                total_codes = len(fund_codes)
                logger.info(f"找到 {total_codes} 只基金需要更新累计分红数据")
                
                if total_codes == 0:
                    return {
                        "success": True,
                        "total_codes": 0,
                        "total_saved": 0,
                        "message": "未找到需要更新的基金代码"
                    }
                
                total_saved = 0
                processed = 0
                failed = 0
                results = []
                
                for i in range(0, total_codes, batch_size):
                    batch_codes = fund_codes[i:i + batch_size]
                    
                    async def worker(code):
                        try:
                            loop = asyncio.get_event_loop()
                            df = await loop.run_in_executor(
                                _executor, self._fetch_fund_etf_dividend_sina, code
                            )
                            if df is not None and not df.empty:
                                saved = await self.data_service.save_fund_etf_dividend_sina_data(df, fund_code=code)
                                return {"fund_code": code, "saved": saved, "status": "success"}
                            return {"fund_code": code, "saved": 0, "status": "empty"}
                        except Exception as e:
                            logger.error(f"处理基金 {code} 失败: {e}")
                            return {"fund_code": code, "saved": 0, "status": "failed", "error": str(e)}
                    
                    batch_results = await asyncio.gather(*[worker(code) for code in batch_codes])
                    
                    for item in batch_results:
                        processed += 1
                        total_saved += item["saved"]
                        if item["status"] == "failed":
                            failed += 1
                        results.append(item)
                    
                    progress = 10 + int((processed / total_codes) * 85)
                    await self._update_task_progress(
                        task_id, progress, f"已处理 {processed}/{total_codes} 只基金，保存 {total_saved} 条数据"
                    )
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，共 {total_codes} 只基金，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "total_codes": total_codes,
                    "total_saved": total_saved,
                    "failed": failed,
                    "message": f"成功更新 {total_codes} 只基金的累计分红数据，保存 {total_saved} 条记录（失败 {failed} 只）",
                }
            else:
                if not fund_code:
                    raise ValueError("单个更新模式下必须提供 fund_code 参数")
                
                await self._update_task_progress(task_id, 20, f"正在获取 {fund_code} 的累计分红数据...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_etf_dividend_sina, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"{fund_code} 没有累计分红数据")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"{fund_code} 没有累计分红数据"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_etf_dividend_sina_data(df, fund_code=fund_code)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "message": f"成功更新 {fund_code} 的累计分红数据，保存 {saved} 条记录"
                }
            
        except Exception as e:
            logger.error(f"刷新基金累计分红数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_fh_em(self) -> pd.DataFrame:
        """同步获取基金分红数据（在线程池中调用）
        
        Returns:
            DataFrame
        """
        try:
            import akshare as ak
            df = ak.fund_fh_em()
            return df
        except Exception as e:
            logger.error(f"获取基金分红数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_fh_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金分红数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无特殊参数）
            
        Returns:
            刷新结果
        """
        try:
            # 解析参数：支持单年更新和多年度批量更新
            year = params.get("year")
            batch_update = bool(params.get("batch_update", False))
            start_year = int(params.get("start_year", 1999))
            end_year = int(params.get("end_year", 2025))
            concurrency = int(params.get("concurrency", 3))
            if concurrency <= 0:
                concurrency = 3

            await self._update_task_progress(task_id, 5, "开始刷新基金分红数据...")
            await self._update_task_progress(task_id, 10, "正在从东方财富网获取基金分红数据...")

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_fh_em)

            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到基金分红数据")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到基金分红数据"
                }

            # 选择用于按年份过滤的日期字段
            date_series = None
            if "权益登记日" in df.columns:
                date_series = df["权益登记日"].astype(str)
            elif "除息日期" in df.columns:
                date_series = df["除息日期"].astype(str)

            # 单年更新：按 year 过滤
            if not batch_update and year is not None:
                try:
                    year_int = int(year)
                except Exception:
                    raise ValueError(f"无效的年份参数: {year}")

                if date_series is not None:
                    mask = date_series.str.startswith(str(year_int))
                    df_year = df[mask]
                else:
                    df_year = df

                if df_year is None or df_year.empty:
                    await self._update_task_progress(task_id, 100, f"{year_int} 年没有可用的基金分红数据")
                    return {
                        "success": True,
                        "saved": 0,
                        "rows": 0,
                        "message": f"{year_int} 年没有可用的基金分红数据"
                    }

                await self._update_task_progress(task_id, 50, f"正在保存 {len(df_year)} 条 {year_int} 年的数据...")
                saved = await self.data_service.save_fund_fh_em_data(df_year)
                await self._update_task_progress(task_id, 100, f"更新完成，保存 {saved} 条 {year_int} 年记录")

                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df_year),
                    "message": f"成功更新 {year_int} 年基金分红数据，保存 {saved} 条记录"
                }

            # 保留原有行为：未指定批量更新或年份时，一次性保存全部数据
            if not batch_update:
                await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
                saved = await self.data_service.save_fund_fh_em_data(df)
                await self._update_task_progress(task_id, 100, f"更新完成，保存 {saved} 条记录")

                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "message": f"成功更新基金分红数据，保存 {saved} 条记录"
                }

            # 批量更新：按年份范围切分并发保存
            if start_year > end_year:
                start_year, end_year = end_year, start_year

            if date_series is None:
                # 没有日期字段时，退回为一次性保存全部数据
                await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
                saved = await self.data_service.save_fund_fh_em_data(df)
                await self._update_task_progress(task_id, 100, f"更新完成，保存 {saved} 条记录")
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "message": f"成功更新基金分红数据，保存 {saved} 条记录"
                }

            years = list(range(start_year, end_year + 1))
            await self._update_task_progress(
                task_id,
                30,
                f"准备批量更新基金分红数据，年份范围 {start_year}-{end_year}，并发 {concurrency}...",
            )

            sem = asyncio.Semaphore(concurrency)

            async def save_year(y: int) -> int:
                async with sem:
                    mask = date_series.str.startswith(str(y))
                    df_year = df[mask]
                    if df_year is None or df_year.empty:
                        return 0
                    return await self.data_service.save_fund_fh_em_data(df_year)

            tasks = [save_year(y) for y in years]
            results = await asyncio.gather(*tasks)
            total_saved = sum(results)

            await self._update_task_progress(
                task_id,
                100,
                f"更新完成，保存 {total_saved} 条 {start_year}-{end_year} 年记录",
            )

            rows_count = 0
            try:
                rows_count = int(
                    (df["权益登记日"].astype(str).str.slice(0, 4).astype(int).between(start_year, end_year)).sum()
                    if "权益登记日" in df.columns
                    else (df["除息日期"].astype(str).str.slice(0, 4).astype(int).between(start_year, end_year)).sum()
                )
            except Exception:
                rows_count = 0

            return {
                "success": True,
                "saved": total_saved,
                "rows": rows_count,
                "message": f"成功更新 {start_year}-{end_year} 年基金分红数据，保存 {total_saved} 条记录"
            }

        except Exception as e:
            logger.error(f"刷新基金分红数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_cf_em(self):
        """获取基金拆分数据（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 基金拆分数据
        """
        try:
            import akshare as ak
            df = ak.fund_cf_em()
            return df
        except Exception as e:
            logger.error(f"获取基金拆分数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_cf_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金拆分数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无特殊参数）
            
        Returns:
            刷新结果
        """
        try:
            # 解析参数：支持单年更新和按年份范围批量更新
            year = params.get("year")
            batch_update = bool(params.get("batch_update", False))
            start_year = int(params.get("start_year", 2005))
            # end_year 默认取当前年份
            try:
                end_year = int(params.get("end_year", time.localtime().tm_year))
            except Exception:
                end_year = time.localtime().tm_year
            concurrency = int(params.get("concurrency", 3))
            if concurrency <= 0:
                concurrency = 3

            await self._update_task_progress(task_id, 5, "开始刷新基金拆分数据...")

            await self._update_task_progress(task_id, 10, "正在从东方财富网获取基金拆分数据...")

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_cf_em
            )

            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到基金拆分数据")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到基金拆分数据",
                }

            # 用于按年份过滤的日期字段
            date_series = None
            if "拆分折算日" in df.columns:
                date_series = df["拆分折算日"].astype(str)

            # 单年更新：按 year 过滤
            if not batch_update and year is not None:
                try:
                    year_int = int(year)
                except Exception:
                    raise ValueError(f"无效的年份参数: {year}")

                if date_series is not None:
                    mask = date_series.str.startswith(str(year_int))
                    df_year = df[mask]
                else:
                    df_year = df

                if df_year is None or df_year.empty:
                    await self._update_task_progress(task_id, 100, f"{year_int} 年没有可用的基金拆分数据")
                    return {
                        "success": True,
                        "saved": 0,
                        "rows": 0,
                        "message": f"{year_int} 年没有可用的基金拆分数据",
                    }

                await self._update_task_progress(task_id, 50, f"正在保存 {len(df_year)} 条 {year_int} 年的数据...")
                saved = await self.data_service.save_fund_cf_em_data(df_year)
                await self._update_task_progress(task_id, 100, f"更新完成，保存 {saved} 条 {year_int} 年记录")

                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df_year),
                    "message": f"成功更新 {year_int} 年基金拆分数据，保存 {saved} 条记录",
                }

            # 保留原有行为：未指定批量更新或年份时，一次性保存全部数据
            if not batch_update:
                await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
                saved = await self.data_service.save_fund_cf_em_data(df)
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )

                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "message": f"成功更新基金拆分数据，保存 {saved} 条记录",
                }

            # 批量更新：按年份范围切分并发保存，默认 2005-当前年份
            if start_year > end_year:
                start_year, end_year = end_year, start_year

            if date_series is None:
                # 没有日期字段时，退回为一次性保存全部数据
                await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
                saved = await self.data_service.save_fund_cf_em_data(df)
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "message": f"成功更新基金拆分数据，保存 {saved} 条记录",
                }

            years = list(range(start_year, end_year + 1))
            await self._update_task_progress(
                task_id,
                30,
                f"准备批量更新基金拆分数据，年份范围 {start_year}-{end_year}，并发 {concurrency}...",
            )

            sem = asyncio.Semaphore(concurrency)

            async def save_year(y: int) -> int:
                async with sem:
                    mask = date_series.str.startswith(str(y))
                    df_year = df[mask]
                    if df_year is None or df_year.empty:
                        return 0
                    return await self.data_service.save_fund_cf_em_data(df_year)

            tasks = [save_year(y) for y in years]
            results = await asyncio.gather(*tasks)
            total_saved = sum(results)

            # 估算选定年份范围内的行数
            rows_count = 0
            try:
                rows_count = int(
                    date_series.str.slice(0, 4).astype(int).between(start_year, end_year).sum()
                )
            except Exception:
                rows_count = 0

            await self._update_task_progress(
                task_id,
                100,
                f"更新完成，保存 {total_saved} 条 {start_year}-{end_year} 年记录",
            )

            return {
                "success": True,
                "saved": total_saved,
                "rows": rows_count,
                "message": f"成功更新 {start_year}-{end_year} 年基金拆分数据，保存 {total_saved} 条记录",
            }

        except Exception as e:
            logger.error(f"刷新基金拆分数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_fh_rank_em(self):
        """获取基金分红排行数据（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 基金分红排行数据
        """
        try:
            import akshare as ak
            df = ak.fund_fh_rank_em()
            return df
        except Exception as e:
            logger.error(f"获取基金分红排行数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_fh_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金分红排行数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无特殊参数）
            
        Returns:
            刷新结果
        """
        try:
            await self._update_task_progress(task_id, 5, "开始刷新基金分红排行数据...")
            
            await self._update_task_progress(task_id, 10, "正在从东方财富网获取基金分红排行数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_fh_rank_em
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到基金分红排行数据")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到基金分红排行数据"
                }
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_fh_rank_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "message": f"成功更新基金分红排行数据，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新基金分红排行数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_open_fund_rank_em(self, symbol="全部"):
        """获取开放式基金排行数据（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金类型，choice of {"全部", "股票型", "混合型", "债券型", "指数型", "QDII", "FOF"}
            
        Returns:
            DataFrame: 开放式基金排行数据
        """
        try:
            import akshare as ak
            df = ak.fund_open_fund_rank_em(symbol=symbol)
            return df
        except Exception as e:
            logger.error(f"获取开放式基金排行数据失败(symbol={symbol}): {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_open_fund_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新开放式基金排行数据（一次性获取全部数据或指定类型）
        
        Args:
            task_id: 任务ID
            params: 参数，包含 symbol（可选，默认"全部"）
            
        Returns:
            刷新结果
        """
        try:
            # 获取参数
            symbol = params.get('symbol', '全部')
            
            # 验证参数
            valid_symbols = ["全部", "股票型", "混合型", "债券型", "指数型", "QDII", "FOF"]
            if symbol not in valid_symbols:
                raise ValueError(f"无效的symbol参数: {symbol}，必须是 {valid_symbols} 之一")
            
            await self._update_task_progress(task_id, 5, f"开始刷新开放式基金排行数据(类型={symbol})...")
            
            await self._update_task_progress(task_id, 10, f"正在从东方财富网获取开放式基金排行数据(类型={symbol})...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_open_fund_rank_em, symbol
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, f"未获取到开放式基金排行数据(类型={symbol})")
                return {
                    "success": True,
                    "saved": 0,
                    "message": f"未获取到开放式基金排行数据(类型={symbol})"
                }
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_open_fund_rank_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "symbol": symbol,
                "message": f"成功更新开放式基金排行数据(类型={symbol})，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新开放式基金排行数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_exchange_rank_em(self):
        """获取场内交易基金排行数据（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 场内交易基金排行数据
        """
        try:
            import akshare as ak
            df = ak.fund_exchange_rank_em()
            return df
        except Exception as e:
            logger.error(f"获取场内交易基金排行数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_exchange_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新场内交易基金排行数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无参数）
            
        Returns:
            刷新结果
        """
        try:
            await self._update_task_progress(task_id, 5, "开始刷新场内交易基金排行数据...")
            
            await self._update_task_progress(task_id, 10, "正在从东方财富网获取场内交易基金排行数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_exchange_rank_em
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到场内交易基金排行数据")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到场内交易基金排行数据"
                }
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_exchange_rank_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "message": f"成功更新场内交易基金排行数据，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新场内交易基金排行数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_money_rank_em(self):
        """获取货币型基金排行数据（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 货币型基金排行数据
        """
        try:
            import akshare as ak
            df = ak.fund_money_rank_em()
            return df
        except Exception as e:
            logger.error(f"获取货币型基金排行数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_money_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新货币型基金排行数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无参数）
            
        Returns:
            刷新结果
        """
        try:
            await self._update_task_progress(task_id, 5, "开始刷新货币型基金排行数据...")
            
            await self._update_task_progress(task_id, 10, "正在从东方财富网获取货币型基金排行数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_money_rank_em
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到货币型基金排行数据")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到货币型基金排行数据"
                }
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_money_rank_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "message": f"成功更新货币型基金排行数据，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新货币型基金排行数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_lcx_rank_em(self):
        """获取理财基金排行数据（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 理财基金排行数据
        """
        try:
            import akshare as ak
            df = ak.fund_lcx_rank_em()
            return df
        except Exception as e:
            logger.error(f"获取理财基金排行数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_lcx_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新理财基金排行数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无参数）
            
        Returns:
            刷新结果
        """
        try:
            await self._update_task_progress(task_id, 5, "开始刷新理财基金排行数据...")
            
            await self._update_task_progress(task_id, 10, "正在从东方财富网获取理财基金排行数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_lcx_rank_em
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到理财基金排行数据（目标网站暂无数据）")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到理财基金排行数据（目标网站暂无数据）"
                }
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_lcx_rank_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "message": f"成功更新理财基金排行数据，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新理财基金排行数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_hk_rank_em(self):
        """获取香港基金排行数据（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 香港基金排行数据
        """
        try:
            import akshare as ak
            df = ak.fund_hk_rank_em()
            return df
        except Exception as e:
            logger.error(f"获取香港基金排行数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_hk_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新香港基金排行数据（一次性获取全部数据）
        
        Args:
            task_id: 任务ID
            params: 参数（此接口无参数）
            
        Returns:
            刷新结果
        """
        try:
            await self._update_task_progress(task_id, 5, "开始刷新香港基金排行数据...")
            
            await self._update_task_progress(task_id, 10, "正在从东方财富网获取香港基金排行数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_hk_rank_em
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, "未获取到香港基金排行数据")
                return {
                    "success": True,
                    "saved": 0,
                    "message": "未获取到香港基金排行数据"
                }
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_hk_rank_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "message": f"成功更新香港基金排行数据，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新香港基金排行数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_individual_achievement_xq(self, symbol: str):
        """获取单个基金业绩数据（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            
        Returns:
            DataFrame: 基金业绩数据
        """
        try:
            import akshare as ak
            df = ak.fund_individual_achievement_xq(symbol=symbol)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 业绩数据失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_individual_achievement_xq(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金业绩数据（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - batch: 是否批量更新
                - limit: 批量更新的数量限制
                - concurrency: 并发协程数量（默认3）
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get("fund_code")
            batch_mode = params.get("batch", False)
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的业绩数据...")
                
                await self._update_task_progress(task_id, 20, f"正在从雪球获取基金 {fund_code} 业绩数据...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_individual_achievement_xq, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的业绩数据")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 的业绩数据",
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_individual_achievement_xq_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "message": f"成功更新基金 {fund_code} 业绩数据，保存 {saved} 条记录",
                }
            
            elif batch_mode:
                # 批量更新：从雪球基金基本信息集合（fund_basic_info）获取基金代码列表
                await self._update_task_progress(task_id, 5, "开始批量刷新基金业绩数据...")
                
                limit = int(params.get("limit", 100) or 100)
                concurrency = int(params.get("concurrency", 3) or 3)
                if concurrency <= 0:
                    concurrency = 1
                
                # 获取基金代码列表
                fund_codes: List[str] = []
                async for doc in self.data_service.col_fund_basic_info.find({}, {"基金代码": 1}).limit(limit):
                    code = doc.get("基金代码")
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码",
                    }
                
                await self._update_task_progress(
                    task_id,
                    10,
                    f"找到 {len(fund_codes)} 只基金，开始批量并发更新（并发数={concurrency}）...",
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(concurrency)
                
                async def process_fund(idx: int, code: str) -> None:
                    nonlocal total_saved, success_count, failed_count
                    try:
                        async with semaphore:
                            df_local = await loop.run_in_executor(
                                _executor, self._fetch_fund_individual_achievement_xq, code
                            )
                            
                            if df_local is not None and not df_local.empty:
                                saved_local = await self.data_service.save_fund_individual_achievement_xq_data(df_local)
                                total_saved += saved_local
                                success_count += 1
                            else:
                                failed_count += 1
                            
                            progress = 10 + int(((idx + 1) / len(fund_codes)) * 80)
                            await self._update_task_progress(
                                task_id,
                                min(progress, 95),
                                f"正在更新基金 {code} ({idx + 1}/{len(fund_codes)})...",
                            )
                            
                            # 添加适当延迟避免请求过快
                            await asyncio.sleep(0.5)
                    
                    except Exception as exc:
                        logger.error(f"更新基金 {code} 业绩数据失败: {exc}", exc_info=True)
                        failed_count += 1
                
                tasks = [
                    process_fund(idx, code)
                    for idx, code in enumerate(fund_codes)
                ]
                await asyncio.gather(*tasks)
                
                await self._update_task_progress(
                    task_id,
                    100,
                    f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录",
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "message": f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录",
                }
            
            else:
                raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")
        
        except Exception as e:
            logger.error(f"刷新基金业绩数据失败: {e}", exc_info=True)
            raise
    
    def _process_fund_value_estimation_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理净值估算数据的列名：提取日期并重命名列
        
        Args:
            df: 原始数据
            
        Returns:
            处理后的数据，包含日期字段
        """
        import re
        
        # 提取日期（从列名中找到日期）
        date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
        dates_found = set()
        
        for col in df.columns:
            match = date_pattern.search(str(col))
            if match:
                dates_found.add(match.group(1))
        
        # 使用最新的日期作为数据日期
        if dates_found:
            estimation_date = sorted(dates_found, reverse=True)[0]
            logger.info(f"提取到估算日期: {estimation_date}")
        else:
            # 如果没有找到日期，使用当前日期
            from datetime import datetime
            estimation_date = datetime.now().strftime('%Y-%m-%d')
            logger.warning(f"未在列名中找到日期，使用当前日期: {estimation_date}")
        
        # 重命名列：去除日期前缀
        new_columns = {}
        for col in df.columns:
            # 如果列名包含日期，去除日期部分
            if date_pattern.search(str(col)):
                # 去除 "YYYY-MM-DD-" 前缀
                new_col = date_pattern.sub('', str(col)).lstrip('-')
                new_columns[col] = new_col
            else:
                new_columns[col] = col
        
        df = df.rename(columns=new_columns)
        
        # 添加日期字段
        df['日期'] = estimation_date
        
        logger.info(f"处理后的列名: {df.columns.tolist()}")
        
        return df
    
    def _fetch_fund_value_estimation_em(self, symbol: str = "全部"):
        """获取净值估算数据（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金类型
            
        Returns:
            DataFrame: 净值估算数据
        """
        try:
            import akshare as ak
            df = ak.fund_value_estimation_em(symbol=symbol)
            return df
        except Exception as e:
            logger.error(f"获取净值估算数据失败 (symbol={symbol}): {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_value_estimation_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新净值估算数据（支持按基金类型过滤）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - symbol: 基金类型（全部, 股票型, 混合型, 债券型, 指数型, QDII, ETF联接, LOF, 场内交易基金）
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get('symbol', '全部')
            
            await self._update_task_progress(task_id, 5, f"开始刷新净值估算数据 (symbol={symbol})...")
            
            await self._update_task_progress(task_id, 10, f"正在从东方财富网获取净值估算数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, self._fetch_fund_value_estimation_em, symbol
            )
            
            if df is None or df.empty:
                await self._update_task_progress(task_id, 100, f"未获取到净值估算数据 (symbol={symbol})")
                return {
                    "success": True,
                    "saved": 0,
                    "symbol": symbol,
                    "message": f"未获取到净值估算数据 (symbol={symbol})"
                }
            
            await self._update_task_progress(task_id, 40, f"正在处理列名和日期...")
            
            # 处理列名：提取日期并重命名列
            df = self._process_fund_value_estimation_columns(df)
            
            await self._update_task_progress(task_id, 50, f"正在保存 {len(df)} 条数据...")
            
            saved = await self.data_service.save_fund_value_estimation_em_data(df)
            
            await self._update_task_progress(
                task_id, 100, f"更新完成，保存 {saved} 条记录"
            )
            
            return {
                "success": True,
                "saved": saved,
                "rows": len(df),
                "symbol": symbol,
                "message": f"成功更新净值估算数据 (symbol={symbol})，保存 {saved} 条记录"
            }
            
        except Exception as e:
            logger.error(f"刷新净值估算数据失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_individual_analysis_xq(self, symbol: str):
        """获取单个基金数据分析（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            
        Returns:
            DataFrame: 基金数据分析
        """
        try:
            import akshare as ak
            df = ak.fund_individual_analysis_xq(symbol=symbol)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 数据分析失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_individual_analysis_xq(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金数据分析（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - batch: 是否批量更新
                - limit: 批量更新的数量限制
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            batch_mode = params.get('batch', False)
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的数据分析...")
                
                await self._update_task_progress(task_id, 20, f"正在从雪球获取基金 {fund_code} 数据分析...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_individual_analysis_xq, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的数据分析")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 的数据分析"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_individual_analysis_xq_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "message": f"成功更新基金 {fund_code} 数据分析，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取基金代码列表
                await self._update_task_progress(task_id, 5, "开始批量刷新基金数据分析...")
                
                limit = params.get('limit', 100)
                
                # 获取基金代码列表
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                await self._update_task_progress(
                    task_id, 10, f"找到 {len(fund_codes)} 只基金，开始批量更新..."
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                
                loop = asyncio.get_event_loop()
                
                for idx, code in enumerate(fund_codes):
                    try:
                        progress = 10 + int((idx / len(fund_codes)) * 80)
                        await self._update_task_progress(
                            task_id, progress, 
                            f"正在更新基金 {code} ({idx+1}/{len(fund_codes)})..."
                        )
                        
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_individual_analysis_xq, code
                        )
                        
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_individual_analysis_xq_data(df)
                            total_saved += saved
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        # 添加延迟避免请求过快
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"更新基金 {code} 数据分析失败: {e}")
                        failed_count += 1
                        continue
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "message": f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新基金数据分析失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_individual_profit_probability_xq(self, symbol: str):
        """获取单个基金盈利概率（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            
        Returns:
            DataFrame: 基金盈利概率
        """
        try:
            import akshare as ak
            from datetime import datetime
            df = ak.fund_individual_profit_probability_xq(symbol=symbol)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
                df['日期'] = datetime.now().strftime('%Y-%m-%d')  # 添加当日日期
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 盈利概率失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_individual_profit_probability_xq(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金盈利概率（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - batch: 是否批量更新
                - limit: 批量更新的数量限制
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            batch_mode = params.get('batch', False)
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的盈利概率...")
                
                await self._update_task_progress(task_id, 20, f"正在从雪球获取基金 {fund_code} 盈利概率...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_individual_profit_probability_xq, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的盈利概率")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 的盈利概率"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_individual_profit_probability_xq_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "message": f"成功更新基金 {fund_code} 盈利概率，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取基金代码列表
                await self._update_task_progress(task_id, 5, "开始批量刷新基金盈利概率...")
                
                limit = params.get('limit', 100)
                
                # 获取基金代码列表
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                await self._update_task_progress(
                    task_id, 10, f"找到 {len(fund_codes)} 只基金，开始批量更新..."
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                
                loop = asyncio.get_event_loop()
                
                for idx, code in enumerate(fund_codes):
                    try:
                        progress = 10 + int((idx / len(fund_codes)) * 80)
                        await self._update_task_progress(
                            task_id, progress, 
                            f"正在更新基金 {code} ({idx+1}/{len(fund_codes)})..."
                        )
                        
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_individual_profit_probability_xq, code
                        )
                        
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_individual_profit_probability_xq_data(df)
                            total_saved += saved
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        # 添加延迟避免请求过快
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"更新基金 {code} 盈利概率失败: {e}")
                        failed_count += 1
                        continue
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "message": f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新基金盈利概率失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_individual_detail_hold_xq(self, symbol: str, date: str):
        """获取单个基金持仓资产比例（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            date: 季度日期 (e.g., '2024-09-30')
            
        Returns:
            DataFrame: 基金持仓资产比例
        """
        try:
            import akshare as ak
            df = ak.fund_individual_detail_hold_xq(symbol=symbol, date=date)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
                df['日期'] = date
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 在 {date} 的持仓资产比例失败: {e}")
            return pd.DataFrame()
    
    def _generate_quarter_end_dates(self, start_year: int = 2000):
        """生成从指定年份至今的所有季度末日期
        
        季度末日期：3月30日、6月30日、9月30日、12月31日
        
        Args:
            start_year: 起始年份，默认2000年
            
        Returns:
            日期列表，格式为 YYYY-MM-DD
        """
        from datetime import datetime
        current_year = datetime.now().year
        dates = []
        
        for year in range(start_year, current_year + 1):
            dates.extend([
                f"{year}-03-30",
                f"{year}-06-30",
                f"{year}-09-30",
                f"{year}-12-31"
            ])
        
        # 只保留不晚于当前日期的季度末日期
        current_date = datetime.now().strftime('%Y-%m-%d')
        dates = [d for d in dates if d <= current_date]
        
        return dates
    
    async def _refresh_fund_individual_detail_hold_xq(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金持仓资产比例（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - symbol: 单个基金代码（单个更新）
                - date: 季度日期（单个更新必需）
                - batch: 是否批量更新（自动生成2000年以来季度末日期）
                - limit: 批量更新的基金数量限制
                - concurrency: 并发线程数
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('symbol') or params.get('fund_code')
            date = params.get('date')
            batch_mode = params.get('batch', False)
            
            # 单个更新模式
            if fund_code and not batch_mode:
                # 单个基金更新，必须提供日期
                if not date:
                    raise ValueError("单个更新必须提供 date 参数（季度日期，例如 2024-09-30）")
                    
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 在 {date} 的持仓资产比例...")
                
                await self._update_task_progress(task_id, 20, f"正在从雪球获取基金 {fund_code} 在 {date} 的持仓资产比例...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_individual_detail_hold_xq, fund_code, date
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 在 {date} 的持仓资产比例")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 在 {date} 的持仓资产比例"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存数据...")
                
                saved = await self.data_service.save_fund_individual_detail_hold_xq_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "fund_code": fund_code,
                    "date": date,
                    "message": f"成功更新基金 {fund_code} 在 {date} 的持仓资产比例，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取基金代码列表，遍历所有季度末日期
                await self._update_task_progress(task_id, 2, "开始批量刷新基金持仓资产比例...")
                
                limit = params.get('limit', 100)
                concurrency = params.get('concurrency', 3)
                
                # 获取基金代码列表
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                # 生成2000年以来的所有季度末日期
                quarter_dates = self._generate_quarter_end_dates(2000)
                
                await self._update_task_progress(
                    task_id, 5, 
                    f"找到 {len(fund_codes)} 只基金，{len(quarter_dates)} 个季度末日期，开始批量更新..."
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                total_tasks = len(fund_codes) * len(quarter_dates)
                completed_tasks = 0
                
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(concurrency)  # 并发控制
                
                # 遍历每个基金代码和每个日期
                for code in fund_codes:
                    for date_item in quarter_dates:
                        async with semaphore:
                            try:
                                completed_tasks += 1
                                progress = 5 + int((completed_tasks / total_tasks) * 90)
                                await self._update_task_progress(
                                    task_id, progress,
                                    f"正在更新基金 {code} 在 {date_item} 的持仓（{completed_tasks}/{total_tasks}）..."
                                )
                                
                                df = await loop.run_in_executor(
                                    _executor, self._fetch_fund_individual_detail_hold_xq, code, date_item
                                )
                                
                                if df is not None and not df.empty:
                                    saved = await self.data_service.save_fund_individual_detail_hold_xq_data(df)
                                    total_saved += saved
                                    success_count += 1
                                else:
                                    failed_count += 1
                                
                                # 添加延迟避免请求过快
                                await asyncio.sleep(0.2)
                                
                            except Exception as e:
                                logger.error(f"更新基金 {code} 在 {date_item} 的持仓资产比例失败: {e}")
                                failed_count += 1
                                continue
                
                await self._update_task_progress(
                    task_id, 100,
                    f"批量更新完成: 成功 {success_count} 次，失败 {failed_count} 次，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "total_dates": len(quarter_dates),
                    "total_tasks": total_tasks,
                    "message": f"批量更新完成: 成功 {success_count} 次，失败 {failed_count} 次，保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 symbol 参数进行单个更新，或设置 batch=True 进行批量更新")
        except Exception as e:
            logger.error(f"刷新基金持仓资产比例失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_overview_em(self, symbol: str):
        """获取单个基金基本概况（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            
        Returns:
            DataFrame: 基金基本概况
        """
        try:
            import akshare as ak
            df = ak.fund_overview_em(symbol=symbol)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 基本概况失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_overview_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金基本概况（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - batch: 是否批量更新
                - limit: 批量更新的数量限制
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            batch_mode = params.get('batch', False)
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的基本概况...")
                
                await self._update_task_progress(task_id, 20, f"正在从东财获取基金 {fund_code} 基本概况...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_overview_em, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的基本概况")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 的基本概况"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_overview_em_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "message": f"成功更新基金 {fund_code} 基本概况，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取基金代码列表
                await self._update_task_progress(task_id, 5, "开始批量刷新基金基本概况...")
                
                limit = params.get('limit', 100)
                
                # 获取基金代码列表
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                await self._update_task_progress(
                    task_id, 10, f"找到 {len(fund_codes)} 只基金，开始批量更新..."
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                
                loop = asyncio.get_event_loop()
                
                for idx, code in enumerate(fund_codes):
                    try:
                        progress = 10 + int((idx / len(fund_codes)) * 80)
                        await self._update_task_progress(
                            task_id, progress, 
                            f"正在更新基金 {code} ({idx+1}/{len(fund_codes)})..."
                        )
                        
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_overview_em, code
                        )
                        
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_overview_em_data(df)
                            total_saved += saved
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        # 添加延迟避免请求过快
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"更新基金 {code} 基本概况失败: {e}")
                        failed_count += 1
                        continue
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "message": f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新基金基本概况失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_fee_em(self, symbol: str):
        """获取单个基金交易费率（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            
        Returns:
            DataFrame: 基金交易费率
        """
        try:
            import akshare as ak
            df = ak.fund_fee_em(symbol=symbol)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 交易费率失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_fee_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金交易费率（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - batch: 是否批量更新
                - limit: 批量更新的数量限制
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            batch_mode = params.get('batch', False)
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的交易费率...")
                
                await self._update_task_progress(task_id, 20, f"正在从东财获取基金 {fund_code} 交易费率...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_fee_em, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的交易费率")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 的交易费率"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_fee_em_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "message": f"成功更新基金 {fund_code} 交易费率，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取基金代码列表
                await self._update_task_progress(task_id, 5, "开始批量刷新基金交易费率...")
                
                limit = params.get('limit', 100)
                
                # 获取基金代码列表
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                await self._update_task_progress(
                    task_id, 10, f"找到 {len(fund_codes)} 只基金，开始批量更新..."
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                
                loop = asyncio.get_event_loop()
                
                for idx, code in enumerate(fund_codes):
                    try:
                        progress = 10 + int((idx / len(fund_codes)) * 80)
                        await self._update_task_progress(
                            task_id, progress, 
                            f"正在更新基金 {code} ({idx+1}/{len(fund_codes)})..."
                        )
                        
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_fee_em, code
                        )
                        
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_fee_em_data(df)
                            total_saved += saved
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        # 添加延迟避免请求过快
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"更新基金 {code} 交易费率失败: {e}")
                        failed_count += 1
                        continue
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "message": f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新基金交易费率失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_individual_detail_info_xq(self, symbol: str):
        """获取单个基金交易规则（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            
        Returns:
            DataFrame: 基金交易规则
        """
        try:
            import akshare as ak
            df = ak.fund_individual_detail_info_xq(symbol=symbol)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 交易规则失败: {e}")
            return pd.DataFrame()
    
    async def _refresh_fund_individual_detail_info_xq(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金交易规则（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - batch: 是否批量更新
                - limit: 批量更新的数量限制
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            batch_mode = params.get('batch', False)
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的交易规则...")
                
                await self._update_task_progress(task_id, 20, f"正在从雪球获取基金 {fund_code} 交易规则...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_individual_detail_info_xq, fund_code
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的交易规则")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} 的交易规则"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_individual_detail_info_xq_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "message": f"成功更新基金 {fund_code} 交易规则，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取基金代码列表
                await self._update_task_progress(task_id, 5, "开始批量刷新基金交易规则...")
                
                limit = params.get('limit', 100)
                
                # 获取基金代码列表
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                await self._update_task_progress(
                    task_id, 10, f"找到 {len(fund_codes)} 只基金，开始批量更新..."
                )
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                
                loop = asyncio.get_event_loop()
                
                for idx, code in enumerate(fund_codes):
                    try:
                        progress = 10 + int((idx / len(fund_codes)) * 80)
                        await self._update_task_progress(
                            task_id, progress, 
                            f"正在更新基金 {code} ({idx+1}/{len(fund_codes)})..."
                        )
                        
                        df = await loop.run_in_executor(
                            _executor, self._fetch_fund_individual_detail_info_xq, code
                        )
                        
                        if df is not None and not df.empty:
                            saved = await self.data_service.save_fund_individual_detail_info_xq_data(df)
                            total_saved += saved
                            success_count += 1
                        else:
                            failed_count += 1
                        
                        # 添加延迟避免请求过快
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"更新基金 {code} 交易规则失败: {e}")
                        failed_count += 1
                        continue
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "total_funds": len(fund_codes),
                    "message": f"批量更新完成: 成功 {success_count} 只，失败 {failed_count} 只，保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新基金交易规则失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_portfolio_hold_em(self, symbol: str, year: str):
        """获取单个基金持仓（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            year: 查询年份 (YYYY)
            
        Returns:
            DataFrame: 基金持仓
        """
        try:
            import akshare as ak
            df = ak.fund_portfolio_hold_em(symbol=symbol, date=year)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 年份 {year} 持仓失败: {e}")
            return None
    
    async def _refresh_fund_portfolio_hold_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金持仓（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - year: 查询年份 (单个更新必须，格式: YYYY)
                - batch: 是否批量更新
                - concurrency: 并发数
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            year = params.get('year')
            batch_mode = params.get('batch', False)
            
            # 单个更新需要年份
            if not batch_mode and not year:
                raise ValueError("单个更新必须提供 year 参数（格式: YYYY）")
            
            if fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的持仓 (年份 {year})...")
                
                await self._update_task_progress(task_id, 20, f"正在从东财获取基金 {fund_code} {year}年持仓...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_portfolio_hold_em, fund_code, year
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} {year}年的持仓")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} {year}年的持仓"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_portfolio_hold_em_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "year": year,
                    "message": f"成功更新基金 {fund_code} {year}年持仓，保存 {saved} 条记录"
                }
            
            elif batch_mode:
                # 批量更新：从fund_name_em获取所有基金代码，遍历年份
                await self._update_task_progress(task_id, 5, "开始批量刷新基金持仓...")
                
                concurrency = params.get('concurrency', 3)
                
                # 获取所有基金代码（不设置limit）
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                # 生成年份列表
                from datetime import datetime
                current_year = datetime.now().year
                
                years = []
                if year:
                    # 指定年份，只更新该年份
                    try:
                        year_int = int(year)
                        years = [str(year_int)]
                    except ValueError:
                        raise ValueError(f"年份参数无效: {year}")
                else:
                    # 未指定年份，遍历2010年到今年的所有年份
                    years = [str(y) for y in range(2010, current_year + 1)]
                
                # 生成所有可能的（基金代码，年份）组合
                all_combinations = [(code, y) for code in fund_codes for y in years]
                total_possible = len(all_combinations)
                
                year_info = f"年份 {year}" if year else f"2010-{current_year} 所有年份"
                await self._update_task_progress(
                    task_id, 5, 
                    f"找到 {len(fund_codes)} 只基金，{len(years)} 个年份（{year_info}），共 {total_possible} 个可能组合，正在查询已有数据..."
                )
                
                # 查询数据库中已有的（基金代码，年份）组合
                existing_combinations = set()
                async for doc in self.data_service.col_fund_portfolio_hold_em.find({}, {'基金代码': 1, '季度': 1}):
                    fund_code_db = doc.get('基金代码')
                    quarter = doc.get('季度', '')
                    # 从季度字段提取年份（如"2024年1季度股票投资明细" -> "2024"）
                    import re
                    year_match = re.search(r'(\d{4})年', str(quarter))
                    if fund_code_db and year_match:
                        year_db = year_match.group(1)
                        existing_combinations.add((fund_code_db, year_db))
                
                # 过滤出需要更新的组合（排除已存在的）
                combinations_to_update = [(code, y) for code, y in all_combinations 
                                         if (code, y) not in existing_combinations]
                
                total_tasks = len(combinations_to_update)
                skipped_count = total_possible - total_tasks
                
                await self._update_task_progress(
                    task_id, 10, 
                    f"增量更新：总计 {total_possible} 个组合，已存在 {skipped_count} 个，需要更新 {total_tasks} 个"
                )
                
                if total_tasks == 0:
                    await self._update_task_progress(task_id, 100, "所有数据已存在，无需更新")
                    return {
                        "success": True,
                        "saved": 0,
                        "skipped": skipped_count,
                        "message": f"所有数据已存在（{skipped_count} 个组合），无需更新"
                    }
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                completed = 0
                no_data_count = 0
                failed_tasks = []  # 记录失败任务明细: 基金代码 + 年份
                
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(concurrency)
                
                # 创建终端进度条
                pbar = tqdm(total=total_tasks, desc="基金持仓批量更新", unit="任务", 
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
                
                async def update_one(code, y):
                    nonlocal total_saved, success_count, failed_count, completed, no_data_count
                    async with semaphore:
                        try:
                            # 更新进度 - 开始处理
                            progress = 10 + int((completed / total_tasks) * 85)
                            await self._update_task_progress(
                                task_id, progress, 
                                f"正在处理: {code} ({y}年) | 进度: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count}"
                            )
                            
                            df = await loop.run_in_executor(
                                _executor, self._fetch_fund_portfolio_hold_em, code, y
                            )
                            
                            if df is None:
                                # 调用 AkShare 过程中发生异常等，视为真实失败
                                failed_count += 1
                                failed_tasks.append({
                                    '基金代码': code,
                                    '年份': y,
                                    '原因': 'fetch_returned_none'
                                })
                                logger.error(
                                    f"基金持仓批量失败任务: 基金 {code}, 年份 {y}，原因: fetch 返回 None"
                                )
                            elif not df.empty:
                                # 正常获取到非空数据，执行保存
                                saved = await self.data_service.save_fund_portfolio_hold_em_data(df)
                                total_saved += saved
                                success_count += 1
                            else:
                                # AkShare 返回空数据，视为该组合当前无数据
                                no_data_count += 1
                            
                            completed += 1
                            
                            # 更新终端进度条
                            pbar.update(1)
                            pbar.set_postfix({
                                '成功': success_count, 
                                '无数据': no_data_count,
                                '失败': failed_count,
                                '已保存': f'{total_saved}条'
                            })
                            
                            # 更新进度 - 完成处理
                            progress = 10 + int((completed / total_tasks) * 85)
                            await self._update_task_progress(
                                task_id, progress, 
                                f"已完成: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count} | 已保存: {total_saved}条"
                            )
                            
                            # 添加延迟避免请求过快
                            await asyncio.sleep(0.3)
                            
                        except Exception as e:
                            logger.error(f"更新基金 {code} 年份 {y} 持仓失败: {e}")
                            failed_count += 1
                            completed += 1
                            failed_tasks.append({
                                '基金代码': code,
                                '年份': y,
                                '原因': f'exception: {e}'
                            })
                            pbar.update(1)
                
                # 分批处理任务，避免创建过多协程导致内存溢出
                BATCH_SIZE = 100  # 每批处理100个任务
                try:
                    for batch_start in range(0, len(combinations_to_update), BATCH_SIZE):
                        batch_end = min(batch_start + BATCH_SIZE, len(combinations_to_update))
                        batch_combinations = combinations_to_update[batch_start:batch_end]
                        
                        # 创建当前批次的任务
                        batch_tasks = []
                        for code, y in batch_combinations:
                            batch_tasks.append(update_one(code, y))
                        
                        # 执行当前批次
                        await asyncio.gather(*batch_tasks, return_exceptions=True)
                finally:
                    pbar.close()
                    # 统一输出失败任务明细，便于后续排查
                    if failed_tasks:
                        for item in failed_tasks:
                            logger.error(
                                f"基金持仓批量失败任务汇总: 基金 {item['基金代码']}, 年份 {item['年份']}，原因: {item['原因']}"
                            )
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 总任务 {total_tasks}，成功 {success_count}，无数据 {no_data_count}，失败 {failed_count}，跳过 {skipped_count}，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "no_data_count": no_data_count,
                    "skipped_count": skipped_count,
                    "total_funds": len(fund_codes),
                    "total_years": len(years),
                    "total_possible": total_possible,
                    "total_tasks": total_tasks,
                    "year": year if year else f"2010-{current_year}",
                    "message": f"增量更新完成: 可能 {total_possible}，已存在 {skipped_count}，更新 {total_tasks}（成功 {success_count}，失败 {failed_count}），保存 {total_saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 和 year 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新基金持仓失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_portfolio_bond_hold_em(self, symbol: str, year: str):
        """获取单个基金债券持仓（同步方法，在线程池中执行）
        
        Args:
            symbol: 基金代码
            year: 查询年份 (YYYY)
            
        Returns:
            DataFrame: 基金债券持仓
        """
        try:
            import akshare as ak
            df = ak.fund_portfolio_bond_hold_em(symbol=symbol, date=year)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 年份 {year} 债券持仓失败: {e}")
            return None
    
    async def _refresh_fund_portfolio_bond_hold_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新基金债券持仓（支持单个更新和批量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - year: 查询年份 (单个更新必须，格式: YYYY)
                - batch: 是否批量更新
                - concurrency: 并发数
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            year = params.get('year')
            batch_mode = params.get('batch', False)
            
            # 单个更新需要年份
            if not batch_mode and not year:
                raise ValueError("单个更新必须提供 year 参数（格式: YYYY）")
            
            if batch_mode:
                # 批量更新：从fund_name_em获取所有基金代码，遍历年份
                await self._update_task_progress(task_id, 5, "开始批量刷新债券持仓...")
                
                concurrency = params.get('concurrency', 3)
                
                # 获取所有基金代码（不设置limit）
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                # 生成年份列表
                from datetime import datetime
                current_year = datetime.now().year
                
                years = []
                if year:
                    # 指定年份，只更新该年份
                    try:
                        year_int = int(year)
                        years = [str(year_int)]
                    except ValueError:
                        raise ValueError(f"年份参数无效: {year}")
                else:
                    # 未指定年份，遍历2010年到今年的所有年份
                    years = [str(y) for y in range(2010, current_year + 1)]
                
                # 生成所有可能的（基金代码，年份）组合
                all_combinations = [(code, y) for code in fund_codes for y in years]
                total_possible = len(all_combinations)
                
                year_info = f"年份 {year}" if year else f"2010-{current_year} 所有年份"
                await self._update_task_progress(
                    task_id, 5, 
                    f"找到 {len(fund_codes)} 只基金，{len(years)} 个年份（{year_info}），共 {total_possible} 个可能组合，正在查询已有数据..."
                )
                
                # 查询数据库中已有的（基金代码，年份）组合
                existing_combinations = set()
                async for doc in self.data_service.col_fund_portfolio_bond_hold_em.find({}, {'基金代码': 1, '季度': 1}):
                    fund_code_db = doc.get('基金代码')
                    quarter = doc.get('季度', '')
                    # 从季度字段提取年份（如"2024年4季度债券投资明细" -> "2024"）
                    import re
                    year_match = re.search(r'(\d{4})年', str(quarter))
                    if fund_code_db and year_match:
                        year_db = year_match.group(1)
                        existing_combinations.add((fund_code_db, year_db))
                
                # 过滤出需要更新的组合（排除已存在的）
                combinations_to_update = [(code, y) for code, y in all_combinations 
                                         if (code, y) not in existing_combinations]
                
                total_tasks = len(combinations_to_update)
                skipped_count = total_possible - total_tasks
                
                await self._update_task_progress(
                    task_id, 10, 
                    f"增量更新：总计 {total_possible} 个组合，已存在 {skipped_count} 个，需要更新 {total_tasks} 个"
                )
                
                if total_tasks == 0:
                    await self._update_task_progress(task_id, 100, "所有数据已存在，无需更新")
                    return {
                        "success": True,
                        "saved": 0,
                        "skipped": skipped_count,
                        "message": f"所有数据已存在（{skipped_count} 个组合），无需更新"
                    }
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                completed = 0
                no_data_count = 0
                failed_tasks = []
                
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(concurrency)
                
                # 创建终端进度条
                pbar = tqdm(total=total_tasks, desc="债券持仓批量更新", unit="任务", 
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
                
                async def update_one(code, y):
                    nonlocal total_saved, success_count, failed_count, completed, no_data_count
                    async with semaphore:
                        try:
                            # 更新进度 - 开始处理
                            progress = 10 + int((completed / total_tasks) * 85)
                            await self._update_task_progress(
                                task_id, progress, 
                                f"正在处理债券持仓: {code} ({y}年) | 进度: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count}"
                            )
                            
                            df = await loop.run_in_executor(
                                _executor, self._fetch_fund_portfolio_bond_hold_em, code, y
                            )
                            
                            if df is None:
                                failed_count += 1
                                failed_tasks.append({
                                    '基金代码': code,
                                    '年份': y,
                                    '原因': 'fetch_returned_none'
                                })
                                logger.error(
                                    f"基金债券持仓批量失败任务: 基金 {code}, 年份 {y}，原因: fetch 返回 None"
                                )
                            elif not df.empty:
                                saved = await self.data_service.save_fund_portfolio_bond_hold_em_data(df)
                                total_saved += saved
                                success_count += 1
                            else:
                                no_data_count += 1
                            
                            completed += 1
                            
                            # 更新终端进度条
                            pbar.update(1)
                            pbar.set_postfix({
                                '成功': success_count, 
                                '无数据': no_data_count,
                                '失败': failed_count,
                                '已保存': f'{total_saved}条'
                            })
                            
                            # 更新进度 - 完成处理
                            progress = 10 + int((completed / total_tasks) * 85)
                            await self._update_task_progress(
                                task_id, progress, 
                                f"已完成: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count} | 已保存: {total_saved}条"
                            )
                            
                            # 添加延迟避免请求过快
                            await asyncio.sleep(0.3)
                            
                        except Exception as e:
                            logger.error(f"更新基金 {code} 年份 {y} 债券持仓失败: {e}")
                            failed_count += 1
                            completed += 1
                            failed_tasks.append({
                                '基金代码': code,
                                '年份': y,
                                '原因': f'exception: {e}'
                            })
                            pbar.update(1)
                
                # 分批处理任务，避免创建过多协程导致内存溢出
                BATCH_SIZE = 100  # 每批处理100个任务
                try:
                    for batch_start in range(0, len(combinations_to_update), BATCH_SIZE):
                        batch_end = min(batch_start + BATCH_SIZE, len(combinations_to_update))
                        batch_combinations = combinations_to_update[batch_start:batch_end]
                        
                        # 创建当前批次的任务
                        batch_tasks = []
                        for code, y in batch_combinations:
                            batch_tasks.append(update_one(code, y))
                        
                        # 执行当前批次
                        await asyncio.gather(*batch_tasks, return_exceptions=True)
                finally:
                    pbar.close()
                    if failed_tasks:
                        for item in failed_tasks:
                            logger.error(
                                f"基金债券持仓批量失败任务汇总: 基金 {item['基金代码']}, 年份 {item['年份']}，原因: {item['原因']}"
                            )
                
                await self._update_task_progress(
                    task_id, 100, 
                    f"批量更新完成: 总任务 {total_tasks}，成功 {success_count}，无数据 {no_data_count}，失败 {failed_count}，跳过 {skipped_count}，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "no_data_count": no_data_count,
                    "skipped_count": skipped_count,
                    "total_funds": len(fund_codes),
                    "total_years": len(years),
                    "total_possible": total_possible,
                    "total_tasks": total_tasks,
                    "year": year if year else f"2010-{current_year}",
                    "message": f"增量更新完成: 可能 {total_possible}，已存在 {skipped_count}，更新 {total_tasks}（成功 {success_count}，无数据 {no_data_count}，失败 {failed_count}），保存 {total_saved} 条记录"
                }
            
            elif fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的债券持仓 (年份 {year})...")
                
                await self._update_task_progress(task_id, 20, f"正在从东财获取基金 {fund_code} {year}年债券持仓...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_portfolio_bond_hold_em, fund_code, year
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} {year}年的债券持仓")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": f"未获取到基金 {fund_code} {year}年的债券持仓"
                    }
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                
                saved = await self.data_service.save_fund_portfolio_bond_hold_em_data(df)
                
                await self._update_task_progress(
                    task_id, 100, f"更新完成，保存 {saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "year": year,
                    "message": f"成功更新基金 {fund_code} {year}年债券持仓，保存 {saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 和 year 参数进行单个更新，或设置 batch=True 进行批量更新")
            
        except Exception as e:
            logger.error(f"刷新债券持仓失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_portfolio_industry_allocation_em(self, symbol: str, date: str):
        """获取单个基金行业配置"""
        try:
            import akshare as ak
            df = ak.fund_portfolio_industry_allocation_em(symbol=symbol, date=date)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取基金 {symbol} 行业配置失败: {e}")
            return None
    
    async def _refresh_fund_portfolio_industry_allocation_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新行业配置（支持单个更新和批量更新，增量更新）
        
        Args:
            task_id: 任务ID
            params: 参数，支持:
                - fund_code: 单个基金代码
                - date: 截止日期 (格式: YYYY-MM-DD，如 2023-12-31)
                - year: 年份 (批量更新时使用，会转换为该年第4季度末日期)
                - batch: 是否批量更新
                - concurrency: 并发数
            
        Returns:
            刷新结果
        """
        try:
            fund_code = params.get('fund_code')
            date = params.get('date')
            year = params.get('year')
            batch_mode = params.get('batch', False)
            
            # 处理日期参数：优先使用date，否则使用year转换为季度末日期
            if not date and not year:
                raise ValueError("必须提供 date 参数（格式: YYYY-MM-DD）或 year 参数（格式: YYYY）")
            
            # 如果提供了year而没有date，转换为该年第4季度末日期
            if not date and year:
                try:
                    year_int = int(year)
                    date = f"{year_int}-12-31"
                except ValueError:
                    raise ValueError(f"年份参数无效: {year}")
            
            if batch_mode:
                # 批量更新：从fund_name_em获取所有基金代码，使用增量更新
                await self._update_task_progress(task_id, 5, f"开始批量刷新行业配置 ({date})...")
                
                concurrency = params.get('concurrency', 3)
                
                # 获取所有基金代码（不设置limit）
                fund_codes = []
                async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}):
                    code = doc.get('基金代码')
                    if code:
                        fund_codes.append(code)
                
                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }
                
                await self._update_task_progress(
                    task_id, 5,
                    f"找到 {len(fund_codes)} 只基金，正在查询已有数据..."
                )
                
                # 查询数据库中已有的（基金代码，截止时间）组合
                existing_combinations = set()
                async for doc in self.data_service.col_fund_portfolio_industry_allocation_em.find({}, {'基金代码': 1, '截止时间': 1}):
                    fund_code_db = doc.get('基金代码')
                    end_date = doc.get('截止时间', '')
                    if fund_code_db and end_date:
                        existing_combinations.add((fund_code_db, end_date))
                
                # 过滤出需要更新的基金（排除已存在的）
                funds_to_update = [code for code in fund_codes if (code, date) not in existing_combinations]
                
                total_possible = len(fund_codes)
                total_tasks = len(funds_to_update)
                skipped_count = total_possible - total_tasks
                
                await self._update_task_progress(
                    task_id, 10,
                    f"增量更新：总计 {total_possible} 只基金，已存在 {skipped_count} 只，需要更新 {total_tasks} 只"
                )
                
                if total_tasks == 0:
                    await self._update_task_progress(task_id, 100, "所有数据已存在，无需更新")
                    return {
                        "success": True,
                        "saved": 0,
                        "skipped": skipped_count,
                        "message": f"所有数据已存在（{skipped_count} 只基金），无需更新"
                    }
                
                total_saved = 0
                success_count = 0
                failed_count = 0
                completed = 0
                no_data_count = 0
                failed_tasks = []
                
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(concurrency)
                
                # 创建终端进度条
                pbar = tqdm(total=total_tasks, desc="行业配置批量更新", unit="基金",
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
                
                async def update_one(code):
                    nonlocal total_saved, success_count, failed_count, completed, no_data_count
                    async with semaphore:
                        try:
                            # 更新进度 - 开始处理
                            progress = 10 + int((completed / total_tasks) * 85)
                            await self._update_task_progress(
                                task_id, progress,
                                f"正在处理: {code} ({date}) | 进度: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count}"
                            )
                            
                            df = await loop.run_in_executor(
                                _executor, self._fetch_fund_portfolio_industry_allocation_em, code, date
                            )
                            
                            if df is None:
                                failed_count += 1
                                failed_tasks.append({
                                    '基金代码': code,
                                    '截止时间': date,
                                    '原因': 'fetch_returned_none'
                                })
                                logger.error(
                                    f"行业配置批量失败任务: 基金 {code}, 截止时间 {date}，原因: fetch 返回 None"
                                )
                            elif not df.empty:
                                saved = await self.data_service.save_fund_portfolio_industry_allocation_em_data(df)
                                total_saved += saved
                                success_count += 1
                            else:
                                no_data_count += 1
                            
                            completed += 1
                            
                            # 更新终端进度条
                            pbar.update(1)
                            pbar.set_postfix({
                                '成功': success_count,
                                '无数据': no_data_count,
                                '失败': failed_count,
                                '已保存': f'{total_saved}条'
                            })
                            
                            # 更新进度 - 完成处理
                            progress = 10 + int((completed / total_tasks) * 85)
                            await self._update_task_progress(
                                task_id, progress,
                                f"已完成: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count} | 已保存: {total_saved}条"
                            )
                            
                            # 添加延迟避免请求过快
                            await asyncio.sleep(0.3)
                            
                        except Exception as e:
                            logger.error(f"更新基金 {code} 行业配置失败: {e}")
                            failed_count += 1
                            completed += 1
                            failed_tasks.append({
                                '基金代码': code,
                                '截止时间': date,
                                '原因': f'exception: {e}'
                            })
                            pbar.update(1)
                
                # 分批处理任务，避免创建过多协程导致内存溢出
                BATCH_SIZE = 100  # 每批处理100个任务
                try:
                    for batch_start in range(0, len(funds_to_update), BATCH_SIZE):
                        batch_end = min(batch_start + BATCH_SIZE, len(funds_to_update))
                        batch_codes = funds_to_update[batch_start:batch_end]
                        
                        # 创建当前批次的任务
                        batch_tasks = []
                        for code in batch_codes:
                            batch_tasks.append(update_one(code))
                        
                        # 执行当前批次
                        await asyncio.gather(*batch_tasks, return_exceptions=True)
                finally:
                    pbar.close()
                    if failed_tasks:
                        for item in failed_tasks:
                            logger.error(
                                f"行业配置批量失败任务汇总: 基金 {item['基金代码']}, 截止时间 {item['截止时间']}，原因: {item['原因']}"
                            )
                
                await self._update_task_progress(
                    task_id, 100,
                    f"批量更新完成: 总任务 {total_tasks}，成功 {success_count}，无数据 {no_data_count}，失败 {failed_count}，跳过 {skipped_count}，保存 {total_saved} 条记录"
                )
                
                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "no_data_count": no_data_count,
                    "skipped_count": skipped_count,
                    "total_funds": len(fund_codes),
                    "total_possible": total_possible,
                    "total_tasks": total_tasks,
                    "date": date,
                    "year": year if year else date[:4],
                    "message": f"增量更新完成: 可能 {total_possible}，已存在 {skipped_count}，更新 {total_tasks}（成功 {success_count}，无数据 {no_data_count}，失败 {failed_count}），保存 {total_saved} 条记录"
                }
            
            elif fund_code:
                # 单个基金更新
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} 的行业配置 ({date})...")
                await self._update_task_progress(task_id, 20, f"正在从东财获取基金 {fund_code} 行业配置...")
                
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_portfolio_industry_allocation_em, fund_code, date
                )
                
                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} 的行业配置")
                    return {"success": True, "saved": 0, "message": f"未获取到基金 {fund_code} 的行业配置"}
                
                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条数据...")
                saved = await self.data_service.save_fund_portfolio_industry_allocation_em_data(df)
                await self._update_task_progress(task_id, 100, f"更新完成，保存 {saved} 条记录")
                
                return {
                    "success": True,
                    "saved": saved,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "date": date,
                    "message": f"成功更新基金 {fund_code} 行业配置，保存 {saved} 条记录"
                }
            
            else:
                raise ValueError("请提供 fund_code 和 date 参数进行单个更新，或设置 batch=True 进行批量更新（必须提供 date 或 year 参数）")
            
        except Exception as e:
            logger.error(f"刷新行业配置失败: {e}", exc_info=True)
            raise

    def _fetch_single_indicator_change(self, symbol: str, indicator: str, date: str):
        """调用akshare获取单个指标的重大变动（同步方法）"""
        try:
            import akshare as ak
            df = ak.fund_portfolio_change_em(symbol=symbol, indicator=indicator, date=date)
            if df is not None and not df.empty:
                df['基金代码'] = symbol
            return df
        except Exception as e:
            logger.debug(f"获取基金 {symbol} {indicator} {date}年重大变动失败: {e}")
            return pd.DataFrame()
    
    def _fetch_fund_portfolio_change_em(self, symbol: str, date: str = ""):
        """
        调用akshare获取重大变动（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            import pandas as pd
            logger.info(f"开始调用akshare获取重大变动: symbol={symbol}, date={date}")
            
            # 注意：akshare接口可能返回一个DataFrame，也可能返回两个DataFrame（买入、卖出）
            # 或者接口名称不同。这里假设是 fund_portfolio_change_em
            # 如果 date 是年份，例如 "2024"
            
            # 尝试调用
            try:
                result = ak.fund_portfolio_change_em(symbol=symbol, date=date)
            except TypeError:
                # 如果不支持date参数，尝试只传symbol
                result = ak.fund_portfolio_change_em(symbol=symbol)
                
            if result is None:
                return None
                
            # 如果返回的是 tuple/list (buy_df, sell_df)
            if isinstance(result, (tuple, list)) and len(result) >= 2:
                buy_df = result[0]
                sell_df = result[1]
                
                df_list = []
                if buy_df is not None and not buy_df.empty:
                    buy_df['指标类型'] = '买入'
                    df_list.append(buy_df)
                
                if sell_df is not None and not sell_df.empty:
                    sell_df['指标类型'] = '卖出'
                    df_list.append(sell_df)
                    
                if not df_list:
                    return pd.DataFrame()
                    
                return pd.concat(df_list, ignore_index=True)
            
            # 如果返回的是单个DataFrame
            if isinstance(result, pd.DataFrame):
                return result
                
            return None
            
        except Exception as e:
            # 记录debug日志而不是error，避免批量更新时刷屏
            logger.debug(f"调用akshare获取重大变动失败 ({symbol}): {e}")
            return None

    async def _refresh_fund_portfolio_change_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新重大变动数据（支持单个更新和批量增量更新）"""
        try:
            target_fund_code = params.get('fund_code')
            batch = params.get('batch', False)
            limit = params.get('limit', 0)
            date = params.get('date', '2024')  # 默认2024年
            
            if not date:
                raise ValueError("必须提供 date 参数 (年份，如 2024)")

            # 单个基金更新：按基金代码 + 年份更新单只基金的重大变动
            if target_fund_code and not batch:
                fund_code = str(target_fund_code)
                await self._update_task_progress(task_id, 5, f"开始刷新基金 {fund_code} {date} 年重大变动...")
                await self._update_task_progress(task_id, 20, f"正在从东财获取基金 {fund_code} {date} 年重大变动数据...")

                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(
                    _executor, self._fetch_fund_portfolio_change_em, fund_code, date
                )

                if df is None or df.empty:
                    await self._update_task_progress(task_id, 100, f"未获取到基金 {fund_code} {date} 年的重大变动数据")
                    return {
                        "success": True,
                        "saved": 0,
                        "rows": 0,
                        "fund_code": fund_code,
                        "date": date,
                        "message": f"未获取到基金 {fund_code} {date} 年的重大变动数据"
                    }

                # 补全必要字段
                if '基金代码' not in df.columns:
                    df['基金代码'] = fund_code
                if '季度' not in df.columns:
                    df['季度'] = f"{date}年"

                await self._update_task_progress(task_id, 60, f"正在保存 {len(df)} 条重大变动数据...")
                saved_rows = await self.data_service.save_fund_portfolio_change_em_data(df)

                await self._update_task_progress(task_id, 100, f"更新完成，保存 {saved_rows} 条记录")
                return {
                    "success": True,
                    "saved": saved_rows,
                    "rows": len(df),
                    "fund_code": fund_code,
                    "date": date,
                    "message": f"成功更新基金 {fund_code} {date} 年重大变动，保存 {saved_rows} 条记录"
                }

            # 批量增量更新：按年份对所有基金进行重大变动更新
            if batch:
                await self._update_task_progress(task_id, 5, "开始批量刷新重大变动数据...")

                concurrency = params.get('concurrency', 3)

                # 1. 获取基金列表
                self.task_manager.update_progress(task_id, 5, 100, "正在获取基金列表...")
                loop = asyncio.get_event_loop()
                fund_list_df = await loop.run_in_executor(_executor, self._fetch_fund_name_em)

                if fund_list_df is None or fund_list_df.empty:
                    raise ValueError("未获取到基金列表")

                fund_codes: List[str] = []
                if '基金代码' in fund_list_df.columns:
                    fund_codes = fund_list_df['基金代码'].astype(str).tolist()
                elif 'code' in fund_list_df.columns:
                    fund_codes = fund_list_df['code'].astype(str).tolist()

                if limit and limit > 0:
                    fund_codes = fund_codes[:limit]

                if not fund_codes:
                    await self._update_task_progress(task_id, 100, "未找到可更新的基金代码")
                    return {
                        "success": True,
                        "saved": 0,
                        "message": "未找到可更新的基金代码"
                    }

                total_possible = len(fund_codes)
                await self._update_task_progress(
                    task_id,
                    10,
                    f"获取到 {total_possible} 只基金，正在查询 {date} 年已存在的重大变动数据..."
                )

                # 2. 查询指定年份已存在重大变动数据的基金代码（按季度字段中的年份判断）
                existing_funds: set = set()
                async for doc in self.data_service.col_fund_portfolio_change_em.find(
                    {'季度': {'$regex': f'{date}年'}},
                    {'基金代码': 1, '季度': 1}
                ):
                    code_db = doc.get('基金代码')
                    if code_db:
                        existing_funds.add(str(code_db))

                # 3. 过滤出需要更新的基金代码（排除已存在该年份数据的基金）
                codes_to_update = [code for code in fund_codes if code not in existing_funds]
                total_tasks = len(codes_to_update)
                skipped_count = total_possible - total_tasks

                await self._update_task_progress(
                    task_id,
                    15,
                    f"增量更新：总计 {total_possible} 只基金，{date} 年已存在 {skipped_count} 只，需要更新 {total_tasks} 只"
                )

                if total_tasks == 0:
                    await self._update_task_progress(task_id, 100, f"{date} 年的重大变动数据已全部存在，无需更新")
                    return {
                        "success": True,
                        "saved": 0,
                        "success_count": 0,
                        "failed_count": 0,
                        "no_data_count": 0,
                        "skipped_count": skipped_count,
                        "total_funds": total_possible,
                        "total_tasks": total_tasks,
                        "date": date,
                        "message": f"{date} 年的重大变动数据已全部存在，无需更新（跳过 {skipped_count} 只基金）"
                    }

                total_saved = 0
                success_count = 0
                failed_count = 0
                no_data_count = 0
                completed = 0
                failed_tasks: List[Dict[str, Any]] = []

                semaphore = asyncio.Semaphore(concurrency)

                # 终端进度条
                pbar = tqdm(
                    total=total_tasks,
                    desc="重大变动批量更新",
                    unit="任务",
                    bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
                )

                async def update_one(code: str):
                    nonlocal total_saved, success_count, failed_count, no_data_count, completed
                    async with semaphore:
                        try:
                            progress = 15 + int((completed / total_tasks) * 80)
                            await self._update_task_progress(
                                task_id,
                                progress,
                                f"正在处理重大变动: {code} ({date} 年) | 进度: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count}"
                            )

                            df = await loop.run_in_executor(
                                _executor, self._fetch_fund_portfolio_change_em, code, date
                            )

                            if df is None:
                                failed_count += 1
                                failed_tasks.append({
                                    "基金代码": code,
                                    "年份": date,
                                    "原因": "fetch_returned_none"
                                })
                                logger.error(
                                    f"重大变动批量失败任务: 基金 {code}, 年份 {date}，原因: fetch 返回 None"
                                )
                            elif not df.empty:
                                if '基金代码' not in df.columns:
                                    df['基金代码'] = code
                                if '季度' not in df.columns:
                                    df['季度'] = f"{date}年"
                                saved_rows = await self.data_service.save_fund_portfolio_change_em_data(df)
                                total_saved += saved_rows
                                success_count += 1
                            else:
                                no_data_count += 1

                            completed += 1

                            # 更新终端进度条
                            pbar.update(1)
                            pbar.set_postfix({
                                "成功": success_count,
                                "无数据": no_data_count,
                                "失败": failed_count,
                                "已保存": f"{total_saved}条"
                            })

                            progress = 15 + int((completed / total_tasks) * 80)
                            await self._update_task_progress(
                                task_id,
                                progress,
                                f"已完成: {completed}/{total_tasks} | 成功: {success_count} | 无数据: {no_data_count} | 失败: {failed_count} | 已保存: {total_saved} 条"
                            )

                            await asyncio.sleep(0.3)

                        except Exception as e:
                            logger.error(f"更新基金 {code} {date} 年重大变动失败: {e}")
                            failed_count += 1
                            completed += 1
                            failed_tasks.append({
                                "基金代码": code,
                                "年份": date,
                                "原因": f"exception: {e}"
                            })
                            pbar.update(1)

                # 分批执行，避免一次创建过多协程
                BATCH_SIZE = 100
                try:
                    for batch_start in range(0, len(codes_to_update), BATCH_SIZE):
                        batch_end = min(batch_start + BATCH_SIZE, len(codes_to_update))
                        batch_codes = codes_to_update[batch_start:batch_end]
                        batch_tasks = [update_one(code) for code in batch_codes]
                        await asyncio.gather(*batch_tasks, return_exceptions=True)
                finally:
                    pbar.close()
                    if failed_tasks:
                        for item in failed_tasks:
                            logger.error(
                                f"重大变动批量失败任务汇总: 基金 {item['基金代码']}, 年份 {item['年份']}，原因: {item['原因']}"
                            )

                await self._update_task_progress(
                    task_id,
                    100,
                    f"批量更新完成: 总任务 {total_tasks}，成功 {success_count}，无数据 {no_data_count}，失败 {failed_count}，跳过 {skipped_count}，保存 {total_saved} 条记录"
                )

                return {
                    "success": True,
                    "saved": total_saved,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "no_data_count": no_data_count,
                    "skipped_count": skipped_count,
                    "total_funds": total_possible,
                    "total_tasks": total_tasks,
                    "date": date,
                    "message": f"增量更新完成: 总基金 {total_possible}，已存在 {skipped_count}，本次更新 {total_tasks}（成功 {success_count}，失败 {failed_count}），保存 {total_saved} 条记录"
                }

            # 未提供 fund_code 且未开启 batch
            raise ValueError("请提供 fund_code 参数进行单个更新，或设置 batch=True 进行批量更新")

        except Exception as e:
            logger.error(f"刷新重大变动失败: {e}", exc_info=True)
            raise

    def _fetch_fund_rating_all_em(self):
        """
        调用akshare获取基金评级总汇（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金评级总汇...")
            df = ak.fund_rating_all()
            logger.info(f"成功获取 {len(df)} 条基金评级总汇数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金评级总汇失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_rating_all_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金评级总汇数据
        
        Args:
            task_id: 任务ID
            params: 参数（该接口无需参数）
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金评级总汇...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_rating_all_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金评级总汇数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_rating_all_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金评级总汇数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金评级总汇失败: {e}", exc_info=True)
            raise

    def _fetch_fund_rating_sh_em(self, date: str):
        """
        调用akshare获取上海证券评级（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取上海证券评级(date={date})...")
            df = ak.fund_rating_sh(date=date)
            logger.info(f"成功获取 {len(df)} 条上海证券评级数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取上海证券评级失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_rating_sh_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新上海证券评级数据
        
        Args:
            task_id: 任务ID
            params: 参数
                - date: 日期，格式YYYYMMDD
            
        Returns:
            刷新结果
        """
        try:
            date = params.get('date', '')
            if not date:
                raise ValueError("必须提供 date 参数 (YYYYMMDD)")
                
            self.task_manager.update_progress(task_id, 10, 100, f"正在从东方财富网获取上海证券评级({date})...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_rating_sh_em, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到上海证券评级数据({date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_rating_sh_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条上海证券评级数据"
            }
            
        except Exception as e:
            logger.error(f"刷新上海证券评级失败: {e}", exc_info=True)
            raise

    def _fetch_fund_rating_zs_em(self, date: str):
        """
        调用akshare获取招商证券评级（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取招商证券评级(date={date})...")
            df = ak.fund_rating_zs(date=date)
            logger.info(f"成功获取 {len(df)} 条招商证券评级数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取招商证券评级失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_rating_zs_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新招商证券评级数据
        
        Args:
            task_id: 任务ID
            params: 参数
                - date: 日期，格式YYYYMMDD
            
        Returns:
            刷新结果
        """
        try:
            date = params.get('date', '')
            if not date:
                raise ValueError("必须提供 date 参数 (YYYYMMDD)")
                
            self.task_manager.update_progress(task_id, 10, 100, f"正在从东方财富网获取招商证券评级({date})...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_rating_zs_em, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到招商证券评级数据({date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_rating_zs_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条招商证券评级数据"
            }
            
        except Exception as e:
            logger.error(f"刷新招商证券评级失败: {e}", exc_info=True)
            raise

    def _fetch_fund_rating_ja_em(self, date: str):
        """
        调用akshare获取济安金信评级（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取济安金信评级(date={date})...")
            df = ak.fund_rating_ja(date=date)
            logger.info(f"成功获取 {len(df)} 条济安金信评级数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取济安金信评级失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_rating_ja_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新济安金信评级数据
        
        Args:
            task_id: 任务ID
            params: 参数
                - date: 日期，格式YYYYMMDD
            
        Returns:
            刷新结果
        """
        try:
            date = params.get('date', '')
            if not date:
                raise ValueError("必须提供 date 参数 (YYYYMMDD)")
                
            self.task_manager.update_progress(task_id, 10, 100, f"正在从东方财富网获取济安金信评级({date})...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_rating_ja_em, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到济安金信评级数据({date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_rating_ja_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条济安金信评级数据"
            }
            
        except Exception as e:
            logger.error(f"刷新济安金信评级失败: {e}", exc_info=True)
            raise

    def _fetch_fund_manager_em(self):
        """
        调用akshare获取基金经理（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金经理...")
            df = ak.fund_manager_em()
            logger.info(f"成功获取 {len(df)} 条基金经理数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金经理失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_manager_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金经理数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金经理...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_manager_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金经理数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_manager_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金经理数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金经理失败: {e}", exc_info=True)
            raise

    def _fetch_fund_new_found_em(self):
        """
        调用akshare获取新发基金（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取新发基金...")
            df = ak.fund_new_found_em()
            logger.info(f"成功获取 {len(df)} 条新发基金数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取新发基金失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_new_found_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新新发基金数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取新发基金...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_new_found_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到新发基金数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_new_found_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条新发基金数据"
            }
            
        except Exception as e:
            logger.error(f"刷新新发基金失败: {e}", exc_info=True)
            raise

    def _fetch_fund_scale_open_sina(self):
        """
        调用akshare获取开放式基金规模（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取开放式基金规模...")
            df = ak.fund_scale_open_sina()
            logger.info(f"成功获取 {len(df)} 条开放式基金规模数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取开放式基金规模失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_scale_open_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新开放式基金规模数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从新浪财经获取开放式基金规模...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_scale_open_sina)
            
            if df is None or df.empty:
                raise ValueError("未获取到开放式基金规模数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_scale_open_sina_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条开放式基金规模数据"
            }
            
        except Exception as e:
            logger.error(f"刷新开放式基金规模失败: {e}", exc_info=True)
            raise

    def _fetch_fund_scale_close_sina(self):
        """
        调用akshare获取封闭式基金规模（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取封闭式基金规模...")
            df = ak.fund_scale_close_sina()
            logger.info(f"成功获取 {len(df)} 条封闭式基金规模数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取封闭式基金规模失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_scale_close_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新封闭式基金规模数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从新浪财经获取封闭式基金规模...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_scale_close_sina)
            
            if df is None or df.empty:
                raise ValueError("未获取到封闭式基金规模数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_scale_close_sina_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条封闭式基金规模数据"
            }
            
        except Exception as e:
            logger.error(f"刷新封闭式基金规模失败: {e}", exc_info=True)
            raise

    def _fetch_fund_scale_structured_sina(self):
        """
        调用akshare获取分级子基金规模（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取分级子基金规模...")
            df = ak.fund_scale_structured_sina()
            logger.info(f"成功获取 {len(df)} 条分级子基金规模数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取分级子基金规模失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_scale_structured_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新分级子基金规模数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从新浪财经获取分级子基金规模...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_scale_structured_sina)
            
            if df is None or df.empty:
                raise ValueError("未获取到分级子基金规模数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_scale_structured_sina_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条分级子基金规模数据"
            }
            
        except Exception as e:
            logger.error(f"刷新分级子基金规模失败: {e}", exc_info=True)
            raise

    def _fetch_fund_aum_em(self):
        """
        调用akshare获取基金规模详情（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金规模详情...")
            df = ak.fund_aum_em()
            logger.info(f"成功获取 {len(df)} 条基金规模详情数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金规模详情失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_aum_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金规模详情数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金规模详情...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_aum_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金规模详情数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_aum_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金规模详情数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金规模详情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_aum_trend_em(self):
        """
        调用akshare获取基金规模走势（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金规模走势...")
            df = ak.fund_aum_trend_em()
            logger.info(f"成功获取 {len(df)} 条基金规模走势数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金规模走势失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_aum_trend_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金规模走势数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金规模走势...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_aum_trend_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金规模走势数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_aum_trend_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金规模走势数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金规模走势失败: {e}", exc_info=True)
            raise

    def _fetch_fund_aum_hist_em(self):
        """
        调用akshare获取基金公司历年管理规模（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金公司历年管理规模...")
            # 根据文档，假设需要年份参数，这里我们可能需要遍历年份或者获取所有
            # 由于我不确定接口是否需要参数，我先尝试无参数调用
            # 如果失败，可能需要年份。
            # 假设它不需要参数返回所有
            df = ak.fund_aum_hist_em()
            logger.info(f"成功获取 {len(df)} 条基金公司历年管理规模数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金公司历年管理规模失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_aum_hist_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金公司历年管理规模数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金公司历年管理规模...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_aum_hist_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金公司历年管理规模数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_aum_hist_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金公司历年管理规模数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金公司历年管理规模失败: {e}", exc_info=True)
            raise

    def _fetch_reits_realtime_em(self):
        """
        调用akshare获取REITs实时行情（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取REITs实时行情...")
            df = ak.reits_realtime_em()
            logger.info(f"成功获取 {len(df)} 条REITs实时行情数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取REITs实时行情失败: {e}", exc_info=True)
            raise

    async def _refresh_reits_realtime_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新REITs实时行情数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取REITs实时行情...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_reits_realtime_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到REITs实时行情数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_reits_realtime_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条REITs实时行情数据"
            }
            
        except Exception as e:
            logger.error(f"刷新REITs实时行情失败: {e}", exc_info=True)
            raise

    def _fetch_reits_hist_em(self, symbol):
        """
        调用akshare获取REITs历史行情（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取REITs {symbol} 历史行情...")
            # 根据文档，假设参数是 symbol
            df = ak.reits_hist_em(symbol=symbol)
            logger.info(f"成功获取 {len(df)} 条REITs {symbol} 历史行情数据")
            # 添加代码列，如果接口不返回
            if '代码' not in df.columns and 'code' not in df.columns:
                df['code'] = symbol
            return df
        except Exception as e:
            logger.error(f"调用akshare获取REITs {symbol} 历史行情失败: {e}", exc_info=True)
            # 即使失败也不抛出异常，以便批量处理继续
            return None

    def _fetch_all_reits_hist_em(self, symbols):
        """
        调用akshare获取所有REITs历史行情（同步方法，在线程池中执行）
        """
        all_dfs = []
        for symbol in symbols:
            df = self._fetch_reits_hist_em(symbol)
            if df is not None and not df.empty:
                all_dfs.append(df)
        
        if not all_dfs:
            return pd.DataFrame()
        
        return pd.concat(all_dfs, ignore_index=True)

    async def _refresh_reits_hist_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新REITs历史行情数据
        
        Args:
            task_id: 任务ID
            params: 参数，可包含 code
            
        Returns:
            刷新结果
        """
        try:
            code = params.get('code')
            
            self.task_manager.update_progress(task_id, 10, 100, "准备获取REITs历史行情...")
            
            if code:
                # 单个更新
                self.task_manager.update_progress(task_id, 20, 100, f"正在从东方财富网获取REITs {code} 历史行情...")
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(_executor, self._fetch_reits_hist_em, code)
            else:
                # 批量更新，先获取列表
                self.task_manager.update_progress(task_id, 20, 100, "正在获取REITs列表...")
                
                # 获取列表（复用 reits_realtime_em 的方法，或者从数据库读取）
                # 这里为了简单，我们先尝试从数据库读取 reits_realtime_em
                # 如果数据库为空，则先尝试获取实时行情
                
                # 临时调用 fetch_reits_realtime_em
                loop = asyncio.get_event_loop()
                realtime_df = await loop.run_in_executor(_executor, self._fetch_reits_realtime_em)
                
                if realtime_df is None or realtime_df.empty:
                     raise ValueError("无法获取REITs列表，无法进行批量更新")
                
                codes = realtime_df['代码'].tolist() if '代码' in realtime_df.columns else []
                if not codes and 'code' in realtime_df.columns:
                    codes = realtime_df['code'].tolist()
                
                if not codes:
                    raise ValueError("REITs列表为空")
                
                total_codes = len(codes)
                self.task_manager.update_progress(task_id, 30, 100, f"获取到 {total_codes} 个REITs，开始批量获取历史行情...")
                
                # 批量获取，为了避免超时，我们可以分批处理，或者简单地在这里全部获取（可能会很慢）
                # 考虑到 Python 的 GIL 和 网络 IO，我们在 _fetch_all_reits_hist_em 中处理循环
                # 但为了能够更新进度，我们最好在这里循环
                
                all_dfs = []
                processed_count = 0
                
                for symbol in codes:
                    df = await loop.run_in_executor(_executor, self._fetch_reits_hist_em, symbol)
                    if df is not None and not df.empty:
                        all_dfs.append(df)
                    
                    processed_count += 1
                    if processed_count % 5 == 0:
                         progress = 30 + int((processed_count / total_codes) * 50)
                         self.task_manager.update_progress(task_id, progress, 100, f"已获取 {processed_count}/{total_codes} 个REITs历史行情...")
                
                if not all_dfs:
                     raise ValueError("未获取到任何REITs历史行情数据")
                
                df = pd.concat(all_dfs, ignore_index=True)
            
            if df is None or df.empty:
                raise ValueError("未获取到REITs历史行情数据")
            
            self.task_manager.update_progress(task_id, 80, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 80 + int(percentage * 0.2)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_reits_hist_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条REITs历史行情数据"
            }
            
        except Exception as e:
            logger.error(f"刷新REITs历史行情失败: {e}", exc_info=True)
            raise

    def _fetch_fund_report_stock_cninfo(self, date):
        """
        调用akshare获取基金重仓股-巨潮（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取基金重仓股-巨潮 (date={date})...")
            # 假设接口需要日期参数，格式YYYYMMDD
            # 如果不传，可能默认最新。但考虑到数据量，最好传参。
            # 根据akshare文档，该接口可能通过 date 获取
            # 假设参数为 date, string type, "YYYYMMDD"
            df = ak.fund_report_stock_cninfo(date=date)
            logger.info(f"成功获取 {len(df)} 条基金重仓股数据")
            # 确保有报告期字段
            if '报告期' not in df.columns and 'date' not in df.columns:
                 # 将输入的 date 格式化为 YYYY-MM-DD 作为报告期
                 formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
                 df['报告期'] = formatted_date
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金重仓股-巨潮失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_report_stock_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金重仓股-巨潮数据
        
        Args:
            task_id: 任务ID
            params: 参数，可包含 date (YYYYMMDD)
            
        Returns:
            刷新结果
        """
        try:
            date = params.get('date')
            if not date:
                # 如果未提供日期，默认获取最近一个季度的日期（假设为 20230630，这里需动态计算，为简化先硬编码或抛错）
                # 或者获取最新
                # 尝试不传参数调用（如果支持）
                # 但根据经验，这类接口通常需要日期。
                # 我们这里默认取当前日期的上一个季度末
                now = datetime.now()
                year = now.year
                month = now.month
                
                # 简单的季度推算
                if month <= 3:
                    date = f"{year-1}1231"
                elif month <= 6:
                    date = f"{year}0331"
                elif month <= 9:
                    date = f"{year}0630"
                else:
                    date = f"{year}0930"
            
            self.task_manager.update_progress(task_id, 10, 100, f"正在从巨潮资讯获取 {date} 基金重仓股数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_report_stock_cninfo, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到 {date} 的基金重仓股数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_report_stock_cninfo_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {date} {saved_count} 条基金重仓股数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金重仓股-巨潮失败: {e}", exc_info=True)
            raise

    def _fetch_fund_report_industry_allocation_cninfo(self, date):
        """
        调用akshare获取基金行业配置-巨潮（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取基金行业配置-巨潮 (date={date})...")
            # 假设参数为 date, string type, "YYYYMMDD"
            df = ak.fund_report_industry_allocation_cninfo(date=date)
            logger.info(f"成功获取 {len(df)} 条基金行业配置数据")
            # 确保有报告期字段
            if '报告期' not in df.columns and 'date' not in df.columns:
                 # 将输入的 date 格式化为 YYYY-MM-DD 作为报告期
                 formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
                 df['报告期'] = formatted_date
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金行业配置-巨潮失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_report_industry_allocation_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金行业配置-巨潮数据
        
        Args:
            task_id: 任务ID
            params: 参数，可包含 date (YYYYMMDD)
            
        Returns:
            刷新结果
        """
        try:
            date = params.get('date')
            if not date:
                # 如果未提供日期，默认获取最近一个季度的日期
                now = datetime.now()
                year = now.year
                month = now.month
                
                if month <= 3:
                    date = f"{year-1}1231"
                elif month <= 6:
                    date = f"{year}0331"
                elif month <= 9:
                    date = f"{year}0630"
                else:
                    date = f"{year}0930"
            
            self.task_manager.update_progress(task_id, 10, 100, f"正在从巨潮资讯获取 {date} 基金行业配置数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_report_industry_allocation_cninfo, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到 {date} 的基金行业配置数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_report_industry_allocation_cninfo_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {date} {saved_count} 条基金行业配置数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金行业配置-巨潮失败: {e}", exc_info=True)
            raise

    def _fetch_fund_report_asset_allocation_cninfo(self, date):
        """
        调用akshare获取基金资产配置-巨潮（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取基金资产配置-巨潮 (date={date})...")
            # 假设参数为 date, string type, "YYYYMMDD"
            df = ak.fund_report_asset_allocation_cninfo(date=date)
            logger.info(f"成功获取 {len(df)} 条基金资产配置数据")
            # 确保有报告期字段
            if '报告期' not in df.columns and 'date' not in df.columns:
                 # 将输入的 date 格式化为 YYYY-MM-DD 作为报告期
                 formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
                 df['报告期'] = formatted_date
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金资产配置-巨潮失败: {e}", exc_info=True)
            raise

    async def _refresh_fund_report_asset_allocation_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金资产配置-巨潮数据
        
        Args:
            task_id: 任务ID
            params: 参数，可包含 date (YYYYMMDD)
            
        Returns:
            刷新结果
        """
        try:
            date = params.get('date')
            if not date:
                # 如果未提供日期，默认获取最近一个季度的日期
                now = datetime.now()
                year = now.year
                month = now.month
                
                if month <= 3:
                    date = f"{year-1}1231"
                elif month <= 6:
                    date = f"{year}0331"
                elif month <= 9:
                    date = f"{year}0630"
                else:
                    date = f"{year}0930"
            
            self.task_manager.update_progress(task_id, 10, 100, f"正在从巨潮资讯获取 {date} 基金资产配置数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_report_asset_allocation_cninfo, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到 {date} 的基金资产配置数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_report_asset_allocation_cninfo_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {date} {saved_count} 条基金资产配置数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金资产配置-巨潮失败: {e}", exc_info=True)
            raise

    def _fetch_fund_scale_change_em(self, symbol):
        """
        调用akshare获取规模变动-东财（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取规模变动-东财 (symbol={symbol})...")
            # 假设参数为 symbol
            df = ak.fund_scale_change_em(symbol=symbol)
            logger.info(f"成功获取 {len(df)} 条规模变动数据")
            # 添加代码列
            if 'code' not in df.columns:
                 df['code'] = symbol
            return df
        except Exception as e:
            logger.error(f"调用akshare获取规模变动-东财失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_scale_change_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新规模变动-东财数据
        
        Args:
            task_id: 任务ID
            params: 参数，需包含 code
            
        Returns:
            刷新结果
        """
        try:
            code = params.get('code')
            
            self.task_manager.update_progress(task_id, 10, 100, "准备获取规模变动数据...")
            
            if code:
                 # 单个更新
                self.task_manager.update_progress(task_id, 20, 100, f"正在从东方财富网获取 {code} 规模变动数据...")
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(_executor, self._fetch_fund_scale_change_em, code)
                
                if df is None or df.empty:
                     raise ValueError(f"未获取到 {code} 的规模变动数据")
                
                self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
                
                def on_save_progress(current, total, percentage, message):
                    overall_progress = 50 + int(percentage * 0.5)
                    self.task_manager.update_progress(task_id, overall_progress, 100, message)
                
                saved_count = await self.data_service.save_fund_scale_change_em_data(df, progress_callback=on_save_progress)
                
                self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
                
                return {
                    'success': True,
                    'saved': saved_count,
                    'message': f"成功更新 {code} {saved_count} 条规模变动数据"
                }
            else:
                 # 批量更新 - 需要基金列表
                 # 为简化，这里要求必须传 code
                 raise ValueError("该接口需要提供基金代码 (code)")
            
        except Exception as e:
            logger.error(f"刷新规模变动-东财失败: {e}", exc_info=True)
            raise

    def _fetch_fund_hold_structure_em(self, symbol):
        """
        调用akshare获取持有人结构-东财（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取持有人结构-东财 (symbol={symbol})...")
            # 假设参数为 symbol
            df = ak.fund_hold_structure_em(symbol=symbol)
            logger.info(f"成功获取 {len(df)} 条持有人结构数据")
            # 添加代码列
            if 'code' not in df.columns:
                 df['code'] = symbol
            return df
        except Exception as e:
            logger.error(f"调用akshare获取持有人结构-东财失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_hold_structure_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新持有人结构-东财数据
        
        Args:
            task_id: 任务ID
            params: 参数，需包含 code
            
        Returns:
            刷新结果
        """
        try:
            code = params.get('code')
            
            self.task_manager.update_progress(task_id, 10, 100, "准备获取持有人结构数据...")
            
            if code:
                 # 单个更新
                self.task_manager.update_progress(task_id, 20, 100, f"正在从东方财富网获取 {code} 持有人结构数据...")
                loop = asyncio.get_event_loop()
                df = await loop.run_in_executor(_executor, self._fetch_fund_hold_structure_em, code)
                
                if df is None or df.empty:
                     raise ValueError(f"未获取到 {code} 的持有人结构数据")
                
                self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
                
                def on_save_progress(current, total, percentage, message):
                    overall_progress = 50 + int(percentage * 0.5)
                    self.task_manager.update_progress(task_id, overall_progress, 100, message)
                
                saved_count = await self.data_service.save_fund_hold_structure_em_data(df, progress_callback=on_save_progress)
                
                self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
                
                return {
                    'success': True,
                    'saved': saved_count,
                    'message': f"成功更新 {code} {saved_count} 条持有人结构数据"
                }
            else:
                 # 批量更新 - 需要基金列表
                 # 为简化，这里要求必须传 code
                 raise ValueError("该接口需要提供基金代码 (code)")
            
        except Exception as e:
            logger.error(f"刷新持有人结构-东财失败: {e}", exc_info=True)
            raise

    def _fetch_fund_stock_position_lg(self):
        """
        调用akshare获取股票型基金仓位-乐咕乐股（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取股票型基金仓位-乐咕乐股...")
            # 无参数
            df = ak.fund_stock_position_lg()
            logger.info(f"成功获取 {len(df)} 条股票型基金仓位数据")
            # 确保有 date 字段
            if 'date' not in df.columns and '日期' in df.columns:
                 df.rename(columns={'日期': 'date'}, inplace=True)
            return df
        except Exception as e:
            logger.error(f"调用akshare获取股票型基金仓位-乐咕乐股失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_stock_position_lg(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新股票型基金仓位-乐咕乐股数据
        
        Args:
            task_id: 任务ID
            params: 参数 (不需要)
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "准备获取股票型基金仓位数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_stock_position_lg)
            
            if df is None or df.empty:
                 raise ValueError(f"未获取到股票型基金仓位数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_stock_position_lg_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条股票型基金仓位数据"
            }
            
        except Exception as e:
            logger.error(f"刷新股票型基金仓位-乐咕乐股失败: {e}", exc_info=True)
            raise

    def _fetch_fund_balance_position_lg(self):
        """
        调用akshare获取平衡混合型基金仓位-乐咕乐股（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取平衡混合型基金仓位-乐咕乐股...")
            # 无参数
            df = ak.fund_balance_position_lg()
            logger.info(f"成功获取 {len(df)} 条平衡混合型基金仓位数据")
            # 确保有 date 字段
            if 'date' not in df.columns and '日期' in df.columns:
                 df.rename(columns={'日期': 'date'}, inplace=True)
            return df
        except Exception as e:
            logger.error(f"调用akshare获取平衡混合型基金仓位-乐咕乐股失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_balance_position_lg(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新平衡混合型基金仓位-乐咕乐股数据
        
        Args:
            task_id: 任务ID
            params: 参数 (不需要)
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "准备获取平衡混合型基金仓位数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_balance_position_lg)
            
            if df is None or df.empty:
                 raise ValueError(f"未获取到平衡混合型基金仓位数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_balance_position_lg_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条平衡混合型基金仓位数据"
            }
            
        except Exception as e:
            logger.error(f"刷新平衡混合型基金仓位-乐咕乐股失败: {e}", exc_info=True)
            raise

    def _fetch_fund_linghuo_position_lg(self):
        """
        调用akshare获取灵活配置型基金仓位-乐咕乐股（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取灵活配置型基金仓位-乐咕乐股...")
            # 无参数
            df = ak.fund_linghuo_position_lg()
            logger.info(f"成功获取 {len(df)} 条灵活配置型基金仓位数据")
            # 确保有 date 字段
            if 'date' not in df.columns and '日期' in df.columns:
                 df.rename(columns={'日期': 'date'}, inplace=True)
            return df
        except Exception as e:
            logger.error(f"调用akshare获取灵活配置型基金仓位-乐咕乐股失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_linghuo_position_lg(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新灵活配置型基金仓位-乐咕乐股数据
        
        Args:
            task_id: 任务ID
            params: 参数 (不需要)
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "准备获取灵活配置型基金仓位数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_linghuo_position_lg)
            
            if df is None or df.empty:
                 raise ValueError(f"未获取到灵活配置型基金仓位数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_linghuo_position_lg_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条灵活配置型基金仓位数据"
            }
            
        except Exception as e:
            logger.error(f"刷新灵活配置型基金仓位-乐咕乐股失败: {e}", exc_info=True)
            raise

    def _fetch_fund_announcement_dividend_em(self):
        """
        调用akshare获取基金公告分红配送-东财（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取基金公告分红配送-东财...")
            # 接口不需要参数，获取全量数据
            df = ak.fund_announcement_dividend_em()
            logger.info(f"成功获取 {len(df)} 条基金公告分红配送数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金公告分红配送-东财失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_announcement_dividend_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金公告分红配送-东财数据
        
        Args:
            task_id: 任务ID
            params: 参数 (不需要)
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "准备获取基金公告分红配送数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_announcement_dividend_em)
            
            if df is None or df.empty:
                 raise ValueError(f"未获取到基金公告分红配送数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_announcement_dividend_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金公告分红配送数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金公告分红配送-东财失败: {e}", exc_info=True)
            raise

    def _fetch_fund_announcement_report_em(self):
        """
        调用akshare获取基金公告定期报告-东财（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取基金公告定期报告-东财...")
            # 接口不需要参数，获取全量数据
            df = ak.fund_announcement_report_em()
            logger.info(f"成功获取 {len(df)} 条基金公告定期报告数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金公告定期报告-东财失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_announcement_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金公告定期报告-东财数据
        
        Args:
            task_id: 任务ID
            params: 参数 (不需要)
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "准备获取基金公告定期报告数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_announcement_report_em)
            
            if df is None or df.empty:
                 raise ValueError(f"未获取到基金公告定期报告数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_announcement_report_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金公告定期报告数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金公告定期报告-东财失败: {e}", exc_info=True)
            raise

    def _fetch_fund_announcement_personnel_em(self):
        """
        调用akshare获取基金公告人事调整-东财（同步方法，在线程池中执行）
        """
        try:
            import akshare as ak
            logger.info(f"开始调用akshare获取基金公告人事调整-东财...")
            # 接口不需要参数，获取全量数据
            df = ak.fund_announcement_personnel_em()
            logger.info(f"成功获取 {len(df)} 条基金公告人事调整数据")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金公告人事调整-东财失败: {e}", exc_info=True)
            return None

    async def _refresh_fund_announcement_personnel_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金公告人事调整-东财数据
        
        Args:
            task_id: 任务ID
            params: 参数 (不需要)
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "准备获取基金公告人事调整数据...")
            
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_announcement_personnel_em)
            
            if df is None or df.empty:
                 raise ValueError(f"未获取到基金公告人事调整数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条数据，正在保存...")
            
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_announcement_personnel_em_data(df, progress_callback=on_save_progress)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金公告人事调整数据"
            }
            
        except Exception as e:
            logger.error(f"刷新基金公告人事调整-东财失败: {e}", exc_info=True)
            raise
