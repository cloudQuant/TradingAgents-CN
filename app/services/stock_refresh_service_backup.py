"""
股票数据刷新服务
负责调用akshare获取股票数据并保存到数据库
"""
import logging
from typing import Dict, Any
import asyncio

from app.core.database import get_mongo_db
from app.services.stock_data_service import StockDataService
from app.utils.task_manager import get_task_manager
from tradingagents.dataflows.providers.china.akshare import AKShareProvider

logger = logging.getLogger("webapi")


class StockRefreshService:
    """股票数据刷新服务"""
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.data_service = StockDataService()
        self.task_manager = get_task_manager()
        self.provider = AKShareProvider()
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的股票数据集合
        
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
                "stock_sse_summary": self._refresh_stock_sse_summary,
                "stock_szse_summary": self._refresh_stock_szse_summary,
                "stock_szse_area_summary": self._refresh_stock_szse_area_summary,
                "stock_szse_sector_summary": self._refresh_stock_szse_sector_summary,
                "stock_sse_deal_daily": self._refresh_stock_sse_deal_daily,
                "stock_individual_info_em": self._refresh_stock_individual_info_em,
                "stock_individual_basic_info_xq": self._refresh_stock_individual_basic_info_xq,
                "stock_bid_ask_em": self._refresh_stock_bid_ask_em,
                "stock_zh_a_spot_em": self._refresh_stock_zh_a_spot_em,
                "stock_sh_a_spot_em": self._refresh_stock_sh_a_spot_em,
                "stock_sz_a_spot_em": self._refresh_stock_sz_a_spot_em,
                "stock_esg_hz_sina": self._refresh_stock_esg_hz_sina,
                "stock_esg_zd_sina": self._refresh_stock_esg_zd_sina,
                "stock_esg_rft_sina": self._refresh_stock_esg_rft_sina,
                "stock_esg_msci_sina": self._refresh_stock_esg_msci_sina,
                "stock_esg_rate_sina": self._refresh_stock_esg_rate_sina,
                "stock_rank_xzjp_ths": self._refresh_stock_rank_xzjp_ths,
                "stock_rank_ljqd_ths": self._refresh_stock_rank_ljqd_ths,
                "stock_rank_ljqs_ths": self._refresh_stock_rank_ljqs_ths,
                "stock_rank_xxtp_ths": self._refresh_stock_rank_xxtp_ths,
                "stock_rank_xstp_ths": self._refresh_stock_rank_xstp_ths,
                "stock_rank_cxsl_ths": self._refresh_stock_rank_cxsl_ths,
                "stock_rank_cxfl_ths": self._refresh_stock_rank_cxfl_ths,
                "stock_market_activity_legu": self._refresh_stock_market_activity_legu,
                "stock_zt_pool_dtgc_em": self._refresh_stock_zt_pool_dtgc_em,
                "stock_zt_pool_zbgc_em": self._refresh_stock_zt_pool_zbgc_em,
                "stock_zt_pool_sub_new_em": self._refresh_stock_zt_pool_sub_new_em,
                "stock_zt_pool_strong_em": self._refresh_stock_zt_pool_strong_em,
                "stock_zt_pool_previous_em": self._refresh_stock_zt_pool_previous_em,
                "stock_zt_pool_em": self._refresh_stock_zt_pool_em,
                "stock_board_change_em": self._refresh_stock_board_change_em,
                "stock_changes_em": self._refresh_stock_changes_em,
                "stock_hot_rank_relate_em": self._refresh_stock_hot_rank_relate_em,
                "stock_hot_search_baidu": self._refresh_stock_hot_search_baidu,
                "stock_hk_hot_rank_latest_em": self._refresh_stock_hk_hot_rank_latest_em,
                "stock_hot_rank_latest_em": self._refresh_stock_hot_rank_latest_em,
                "stock_inner_trade_xq": self._refresh_stock_inner_trade_xq,
                "stock_hot_keyword_em": self._refresh_stock_hot_keyword_em,
                "stock_hk_hot_rank_detail_realtime_em": self._refresh_stock_hk_hot_rank_detail_realtime_em,
                "stock_hot_rank_detail_realtime_em": self._refresh_stock_hot_rank_detail_realtime_em,
                "stock_sns_sseinfo": self._refresh_stock_sns_sseinfo,
                "stock_irm_ans_cninfo": self._refresh_stock_irm_ans_cninfo,
                "stock_irm_cninfo": self._refresh_stock_irm_cninfo,
                "stock_hk_hot_rank_detail_em": self._refresh_stock_hk_hot_rank_detail_em,
                "stock_hot_rank_detail_em": self._refresh_stock_hot_rank_detail_em,
                "stock_hk_hot_rank_em": self._refresh_stock_hk_hot_rank_em,
                "stock_hot_up_em": self._refresh_stock_hot_up_em,
                "stock_hot_rank_em": self._refresh_stock_hot_rank_em,
                "stock_hot_deal_xq": self._refresh_stock_hot_deal_xq,
                "stock_hot_tweet_xq": self._refresh_stock_hot_tweet_xq,
                "stock_hot_follow_xq": self._refresh_stock_hot_follow_xq,
                "stock_board_industry_hist_min_em": self._refresh_stock_board_industry_hist_min_em,
                "stock_board_industry_hist_em": self._refresh_stock_board_industry_hist_em,
                "stock_board_industry_cons_em": self._refresh_stock_board_industry_cons_em,
                "stock_comment_detail_zhpj_lspf_em": self._refresh_stock_comment_detail_zhpj_lspf_em,
                "stock_comment_detail_scrd_focus_em": self._refresh_stock_comment_detail_scrd_focus_em,
                "stock_comment_detail_scrd_desire_em": self._refresh_stock_comment_detail_scrd_desire_em,
                "stock_comment_detail_scrd_desire_daily_em": self._refresh_stock_comment_detail_scrd_desire_daily_em,
                "stock_hsgt_fund_flow_summary_em": self._refresh_stock_hsgt_fund_flow_summary_em,
                "stock_sgt_settlement_exchange_rate_szse": self._refresh_stock_sgt_settlement_exchange_rate_szse,
                "stock_sgt_settlement_exchange_rate_sse": self._refresh_stock_sgt_settlement_exchange_rate_sse,
                # 需求107-120
                "stock_sgt_reference_exchange_rate_szse": self._refresh_stock_sgt_reference_exchange_rate_szse,
                "stock_sgt_reference_exchange_rate_sse": self._refresh_stock_sgt_reference_exchange_rate_sse,
                "stock_hk_ggt_components_em": self._refresh_stock_hk_ggt_components_em,
                "stock_hsgt_fund_min_em": self._refresh_stock_hsgt_fund_min_em,
                "stock_hsgt_board_rank_em": self._refresh_stock_hsgt_board_rank_em,
                "stock_hsgt_hold_stock_em": self._refresh_stock_hsgt_hold_stock_em,
                "stock_hsgt_stock_statistics_em": self._refresh_stock_hsgt_stock_statistics_em,
                "stock_hsgt_institution_statistics_em": self._refresh_stock_hsgt_institution_statistics_em,
                "stock_hsgt_sh_hk_spot_em": self._refresh_stock_hsgt_sh_hk_spot_em,
                "stock_hsgt_hist_em": self._refresh_stock_hsgt_hist_em,
                "stock_hsgt_individual_em": self._refresh_stock_hsgt_individual_em,
                "stock_hsgt_individual_detail_em": self._refresh_stock_hsgt_individual_detail_em,
                "stock_em_hsgt_north_net_flow_in": self._refresh_stock_em_hsgt_north_net_flow_in,
                "stock_em_hsgt_south_net_flow_in": self._refresh_stock_em_hsgt_south_net_flow_in,
            }
            
            handler = handlers.get(collection_name)
            if not handler:
                raise ValueError(f"不支持的集合名称: {collection_name}")
            
            result = await handler(task_id, params or {})
            
            self.task_manager.complete_task(task_id, result=result)
            return {"success": True, "data": result}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ 刷新集合 {collection_name} 失败: {error_msg}", exc_info=True)
            self.task_manager.fail_task(task_id, error_msg)
            return {"success": False, "error": error_msg}
    
    async def _refresh_stock_sse_summary(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新上海证券交易所-股票数据总貌
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从AKShare获取数据...")
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sse_summary()
            
            if df is None or df.empty:
                raise ValueError("未获取到上海证券交易所数据总貌")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sse_summary(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sse_summary"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新上海证券交易所数据总貌失败: {e}")
            raise
    
    async def _refresh_stock_szse_summary(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新深圳证券交易所-证券类别统计
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 date）
            
        Returns:
            刷新结果
        """
        try:
            # 获取日期参数，默认使用昨天
            from datetime import datetime, timedelta
            date = params.get("date")
            if not date:
                yesterday = datetime.now() - timedelta(days=1)
                date = yesterday.strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从AKShare获取数据 (日期: {date})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_szse_summary(date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到深圳证券交易所证券类别统计 (日期: {date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_szse_summary(df, date)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_szse_summary",
                "date": date
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新深圳证券交易所证券类别统计失败: {e}")
            raise
    
    async def _refresh_stock_szse_area_summary(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新深圳证券交易所-地区交易排序
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 date，格式为年月如"202203"）
            
        Returns:
            刷新结果
        """
        try:
            # 获取日期参数，默认使用上个月
            from datetime import datetime
            date = params.get("date")
            if not date:
                now = datetime.now()
                if now.month == 1:
                    date = f"{now.year - 1}12"
                else:
                    date = f"{now.year}{now.month - 1:02d}"
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从AKShare获取数据 (年月: {date})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_szse_area_summary(date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到深圳证券交易所地区交易排序 (年月: {date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_szse_area_summary(df, date)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_szse_area_summary",
                "date": date
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新深圳证券交易所地区交易排序失败: {e}")
            raise
    
    async def _refresh_stock_szse_sector_summary(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新深圳证券交易所-股票行业成交数据
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 symbol 和 date）
            
        Returns:
            刷新结果
        """
        try:
            # 获取参数
            from datetime import datetime
            symbol = params.get("symbol", "当月")
            date = params.get("date")
            if not date:
                now = datetime.now()
                if now.month == 1:
                    date = f"{now.year - 1}12"
                else:
                    date = f"{now.year}{now.month - 1:02d}"
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从AKShare获取数据 (symbol={symbol}, date={date})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_szse_sector_summary(symbol, date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到深圳证券交易所股票行业成交数据 (symbol={symbol}, date={date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_szse_sector_summary(df, symbol, date)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_szse_sector_summary",
                "symbol": symbol,
                "date": date
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新深圳证券交易所股票行业成交数据失败: {e}")
            raise
    
    async def _refresh_stock_sse_deal_daily(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新上海证券交易所-每日股票情况
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 date）
            
        Returns:
            刷新结果
        """
        try:
            # 获取日期参数
            from datetime import datetime, timedelta
            date = params.get("date")
            if not date:
                yesterday = datetime.now() - timedelta(days=1)
                date = yesterday.strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从AKShare获取数据 (date={date})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sse_deal_daily(date)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到上海证券交易所每日股票情况 (date={date})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sse_deal_daily(df, date)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sse_deal_daily",
                "date": date
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新上海证券交易所每日股票情况失败: {e}")
            raise
    
    async def _refresh_stock_individual_info_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新东方财富-个股信息
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 symbol）
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol")
            if not symbol:
                raise ValueError("必须提供股票代码 symbol")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取数据 (symbol={symbol})..."
            )
            
            # 调用provider获取数据
            data = await self.provider.get_stock_individual_info_em(symbol)
            
            if not data:
                raise ValueError(f"未获取到股票 {symbol} 的个股信息")
            
            self.task_manager.update_progress(task_id, 50, 100, "正在保存数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_individual_info_em(data, symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, "完成！")
            
            return {
                "saved": saved_count,
                "collection": "stock_individual_info_em",
                "symbol": symbol
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新东方财富个股信息失败: {e}")
            raise
    
    async def _refresh_stock_individual_basic_info_xq(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新雪球-个股基础信息
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 symbol）
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol")
            if not symbol:
                raise ValueError("必须提供股票代码 symbol")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从雪球获取数据 (symbol={symbol})..."
            )
            
            # 调用provider获取数据
            data = await self.provider.get_stock_individual_basic_info_xq(symbol)
            
            if not data:
                raise ValueError(f"未获取到股票 {symbol} 的雪球基础信息")
            
            self.task_manager.update_progress(task_id, 50, 100, "正在保存数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_individual_basic_info_xq(data, symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, "完成！")
            
            return {
                "saved": saved_count,
                "collection": "stock_individual_basic_info_xq",
                "symbol": symbol
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新雪球个股基础信息失败: {e}")
            raise
    
    async def _refresh_stock_bid_ask_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新东方财富-行情报价
        
        Args:
            task_id: 任务ID
            params: 参数（必须包含 symbol）
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol")
            if not symbol:
                raise ValueError("必须提供股票代码 symbol")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取数据 (symbol={symbol})..."
            )
            
            # 调用provider获取数据
            data = await self.provider.get_stock_bid_ask_em(symbol)
            
            if not data:
                raise ValueError(f"未获取到股票 {symbol} 的行情报价")
            
            self.task_manager.update_progress(task_id, 50, 100, "正在保存数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_bid_ask_em(data, symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, "完成！")
            
            return {
                "saved": saved_count,
                "collection": "stock_bid_ask_em",
                "symbol": symbol
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新东方财富行情报价失败: {e}")
            raise
    
    async def _refresh_stock_zh_a_spot_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新沪深京A股实时行情
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取沪深京A股实时行情..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zh_a_spot_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到沪深京A股实时行情")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zh_a_spot_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zh_a_spot_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新沪深京A股实时行情失败: {e}")
            raise
    
    async def _refresh_stock_sh_a_spot_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新沪A股实时行情
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取沪A股实时行情..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sh_a_spot_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到沪A股实时行情")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sh_a_spot_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sh_a_spot_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新沪A股实时行情失败: {e}")
            raise
    
    async def _refresh_stock_sz_a_spot_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新深A股实时行情
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取深A股实时行情..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sz_a_spot_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到深A股实时行情")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sz_a_spot_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sz_a_spot_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新深A股实时行情失败: {e}")
            raise
    
    async def _refresh_stock_esg_hz_sina(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新华证指数ESG评级
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从新浪财经获取华证指数ESG评级..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_esg_hz_sina()
            
            if df is None or df.empty:
                raise ValueError("未获取到华证指数ESG评级")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_esg_hz_sina(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_esg_hz_sina"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新华证指数ESG评级失败: {e}")
            raise
    
    async def _refresh_stock_esg_zd_sina(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新秩鼎ESG评级
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从新浪财经获取秩鼎ESG评级..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_esg_zd_sina()
            
            if df is None or df.empty:
                raise ValueError("未获取到秩鼎ESG评级")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_esg_zd_sina(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_esg_zd_sina"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新秩鼎ESG评级失败: {e}")
            raise
    
    async def _refresh_stock_esg_rft_sina(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新路孚特ESG评级
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从新浪财经获取路孚特ESG评级..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_esg_rft_sina()
            
            if df is None or df.empty:
                raise ValueError("未获取到路孚特ESG评级")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_esg_rft_sina(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_esg_rft_sina"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新路孚特ESG评级失败: {e}")
            raise
    
    async def _refresh_stock_esg_msci_sina(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新MSCI ESG评级
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从新浪财经获取MSCI ESG评级..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_esg_msci_sina()
            
            if df is None or df.empty:
                raise ValueError("未获取到MSCI ESG评级")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_esg_msci_sina(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_esg_msci_sina"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新MSCI ESG评级失败: {e}")
            raise
    
    async def _refresh_stock_esg_rate_sina(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新ESG评级数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从新浪财经获取ESG评级数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_esg_rate_sina()
            
            if df is None or df.empty:
                raise ValueError("未获取到ESG评级数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_esg_rate_sina(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_esg_rate_sina"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新ESG评级数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_xzjp_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新险资举牌数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从同花顺获取险资举牌数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_xzjp_ths()
            
            if df is None or df.empty:
                raise ValueError("未获取到险资举牌数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_xzjp_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_xzjp_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新险资举牌数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_ljqd_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新量价齐跌数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从同花顺获取量价齐跌数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_ljqd_ths()
            
            if df is None or df.empty:
                raise ValueError("未获取到量价齐跌数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_ljqd_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_ljqd_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新量价齐跌数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_ljqs_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新量价齐升数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从同花顺获取量价齐升数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_ljqs_ths()
            
            if df is None or df.empty:
                raise ValueError("未获取到量价齐升数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_ljqs_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_ljqs_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新量价齐升数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_xxtp_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新向下突破数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "500日均线")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从同花顺获取向下突破数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_xxtp_ths(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到向下突破数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_xxtp_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_xxtp_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新向下突破数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_xstp_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新向上突破数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "500日均线")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从同花顺获取向上突破数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_xstp_ths(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到向上突破数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_xstp_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_xstp_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新向上突破数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_cxsl_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新持续缩量数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从同花顺获取持续缩量数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_cxsl_ths()
            
            if df is None or df.empty:
                raise ValueError("未获取到持续缩量数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_cxsl_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_cxsl_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新持续缩量数据失败: {e}")
            raise
    
    async def _refresh_stock_rank_cxfl_ths(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新持续放量数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从同花顺获取持续放量数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_rank_cxfl_ths()
            
            if df is None or df.empty:
                raise ValueError("未获取到持续放量数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_rank_cxfl_ths(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_rank_cxfl_ths"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新持续放量数据失败: {e}")
            raise
    
    async def _refresh_stock_market_activity_legu(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新赚钱效应分析数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从乐咕乐股获取赚钱效应分析数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_market_activity_legu()
            
            if df is None or df.empty:
                raise ValueError("未获取到赚钱效应分析数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_market_activity_legu(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_market_activity_legu"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新赚钱效应分析数据失败: {e}")
            raise
    
    async def _refresh_stock_zt_pool_dtgc_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新跌停股池数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            date_str = params.get("date")
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取跌停股池数据 ({date_str})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zt_pool_dtgc_em(date=date_str)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到跌停股池数据 ({date_str})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zt_pool_dtgc_em(df, date_str=date_str)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zt_pool_dtgc_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新跌停股池数据失败: {e}")
            raise
    
    async def _refresh_stock_zt_pool_zbgc_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新炸板股池数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            date_str = params.get("date")
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取炸板股池数据 ({date_str})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zt_pool_zbgc_em(date=date_str)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到炸板股池数据 ({date_str})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zt_pool_zbgc_em(df, date_str=date_str)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zt_pool_zbgc_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新炸板股池数据失败: {e}")
            raise
    
    async def _refresh_stock_zt_pool_sub_new_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新次新股池数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            date_str = params.get("date")
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取次新股池数据 ({date_str})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zt_pool_sub_new_em(date=date_str)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到次新股池数据 ({date_str})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zt_pool_sub_new_em(df, date_str=date_str)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zt_pool_sub_new_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新次新股池数据失败: {e}")
            raise
    
    async def _refresh_stock_zt_pool_strong_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新强势股池数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            date_str = params.get("date")
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取强势股池数据 ({date_str})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zt_pool_strong_em(date=date_str)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到强势股池数据 ({date_str})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zt_pool_strong_em(df, date_str=date_str)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zt_pool_strong_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新强势股池数据失败: {e}")
            raise
    
    async def _refresh_stock_zt_pool_previous_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新昨日涨停股池数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            date_str = params.get("date")
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取昨日涨停股池数据 ({date_str})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zt_pool_previous_em(date=date_str)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到昨日涨停股池数据 ({date_str})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zt_pool_previous_em(df, date_str=date_str)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zt_pool_previous_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新昨日涨停股池数据失败: {e}")
            raise
    
    async def _refresh_stock_zt_pool_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新涨停股池数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            date_str = params.get("date")
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取涨停股池数据 ({date_str})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_zt_pool_em(date=date_str)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到涨停股池数据 ({date_str})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_zt_pool_em(df, date_str=date_str)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_zt_pool_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新涨停股池数据失败: {e}")
            raise
    
    async def _refresh_stock_board_change_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新板块异动详情数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取板块异动详情数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_board_change_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到板块异动详情数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_board_change_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_board_change_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新板块异动详情数据失败: {e}")
            raise
    
    async def _refresh_stock_changes_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新盘口异动数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "大笔买入")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取盘口异动数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_changes_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到盘口异动数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_changes_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_changes_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新盘口异动数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_rank_relate_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新相关股票数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "SZ000665")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取相关股票数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_rank_relate_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到相关股票数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_rank_relate_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_rank_relate_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新相关股票数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_search_baidu(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新热搜股票数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            from datetime import datetime
            symbol = params.get("symbol", "A股")
            date_str = params.get("date")
            time_param = params.get("time", "今日")
            
            if not date_str:
                date_str = datetime.now().strftime("%Y%m%d")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从百度股市通获取热搜股票数据 ({symbol}, {date_str}, {time_param})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_search_baidu(
                symbol=symbol, 
                date=date_str, 
                time=time_param
            )
            
            if df is None or df.empty:
                raise ValueError(f"未获取到热搜股票数据 ({symbol}, {date_str}, {time_param})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_search_baidu(
                df, 
                date_str=date_str,
                time_param=time_param
            )
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_search_baidu"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新热搜股票数据失败: {e}")
            raise
    
    async def _refresh_stock_hk_hot_rank_latest_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新港股个股人气榜最新排名数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "00700")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取港股个股人气榜最新排名数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hk_hot_rank_latest_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到港股个股人气榜最新排名数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hk_hot_rank_latest_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hk_hot_rank_latest_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新港股个股人气榜最新排名数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_rank_latest_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新A股个股人气榜最新排名数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "SZ000665")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取A股个股人气榜最新排名数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_rank_latest_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到A股个股人气榜最新排名数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_rank_latest_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_rank_latest_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新A股个股人气榜最新排名数据失败: {e}")
            raise
    
    async def _refresh_stock_inner_trade_xq(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新内部交易数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从雪球获取内部交易数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_inner_trade_xq()
            
            if df is None or df.empty:
                raise ValueError("未获取到内部交易数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_inner_trade_xq(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_inner_trade_xq"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新内部交易数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_keyword_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新热门关键词数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "SZ000665")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取热门关键词数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_keyword_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到热门关键词数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_keyword_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_keyword_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新热门关键词数据失败: {e}")
            raise
    
    async def _refresh_stock_hk_hot_rank_detail_realtime_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新港股个股人气榜实时变动数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "00700")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取港股个股人气榜实时变动数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hk_hot_rank_detail_realtime_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到港股个股人气榜实时变动数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hk_hot_rank_detail_realtime_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hk_hot_rank_detail_realtime_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新港股个股人气榜实时变动数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_rank_detail_realtime_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新A股个股人气榜实时变动数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "SZ000665")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取A股个股人气榜实时变动数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_rank_detail_realtime_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到A股个股人气榜实时变动数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_rank_detail_realtime_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_rank_detail_realtime_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新A股个股人气榜实时变动数据失败: {e}")
            raise
    
    async def _refresh_stock_sns_sseinfo(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新上证e互动数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "603119")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从上证e互动获取数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sns_sseinfo(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到上证e互动数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sns_sseinfo(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sns_sseinfo"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新上证e互动数据失败: {e}")
            raise
    
    async def _refresh_stock_irm_ans_cninfo(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新互动易-回答数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "1495108801386602496")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从互动易获取回答数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_irm_ans_cninfo(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到互动易-回答数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_irm_ans_cninfo(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_irm_ans_cninfo"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新互动易-回答数据失败: {e}")
            raise
    
    async def _refresh_stock_irm_cninfo(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新互动易-提问数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "002594")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从互动易获取提问数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_irm_cninfo(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到互动易-提问数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_irm_cninfo(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_irm_cninfo"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新互动易-提问数据失败: {e}")
            raise
    
    async def _refresh_stock_hk_hot_rank_detail_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新港股股票热度-历史趋势数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "00700")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取港股股票热度-历史趋势数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hk_hot_rank_detail_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到港股股票热度-历史趋势数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hk_hot_rank_detail_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hk_hot_rank_detail_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新港股股票热度-历史趋势数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_rank_detail_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新A股股票热度-历史趋势及粉丝特征数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "SZ000665")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取A股股票热度-历史趋势及粉丝特征数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_rank_detail_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到A股股票热度-历史趋势及粉丝特征数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_rank_detail_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_rank_detail_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新A股股票热度-历史趋势及粉丝特征数据失败: {e}")
            raise
    
    async def _refresh_stock_hk_hot_rank_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新港股人气榜数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取港股人气榜数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hk_hot_rank_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到港股人气榜数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hk_hot_rank_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hk_hot_rank_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新港股人气榜数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_up_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新飙升榜-A股数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取飙升榜-A股数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_up_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到飙升榜-A股数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_up_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_up_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新飙升榜-A股数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_rank_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新人气榜-A股数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取人气榜-A股数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_rank_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到人气榜-A股数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_rank_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_rank_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新人气榜-A股数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_deal_xq(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新交易排行榜数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "最热门")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从雪球获取交易排行榜数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_deal_xq(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到交易排行榜数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_deal_xq(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_deal_xq"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新交易排行榜数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_tweet_xq(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新讨论排行榜数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "最热门")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从雪球获取讨论排行榜数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_tweet_xq(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到讨论排行榜数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_tweet_xq(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_tweet_xq"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新讨论排行榜数据失败: {e}")
            raise
    
    async def _refresh_stock_hot_follow_xq(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新关注排行榜数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "最热门")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从雪球获取关注排行榜数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hot_follow_xq(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到关注排行榜数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hot_follow_xq(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hot_follow_xq"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新关注排行榜数据失败: {e}")
            raise
    
    async def _refresh_stock_board_industry_hist_min_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新东方财富-指数-分时数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "小金属")
            period = params.get("period", "1")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取指数-分时数据 ({symbol}, {period})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_board_industry_hist_min_em(symbol=symbol, period=period)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到东方财富-指数-分时数据 ({symbol}, {period})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_board_industry_hist_min_em(df, symbol=symbol, period=period)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_board_industry_hist_min_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新东方财富-指数-分时数据失败: {e}")
            raise
    
    async def _refresh_stock_board_industry_hist_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新东方财富-指数-日频数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "小金属")
            start_date = params.get("start_date", "20211201")
            end_date = params.get("end_date", "20220401")
            period = params.get("period", "日k")
            adjust = params.get("adjust", "")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取指数-日频数据 ({symbol}, {period}, {adjust})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_board_industry_hist_em(
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date, 
                period=period, 
                adjust=adjust
            )
            
            if df is None or df.empty:
                raise ValueError(f"未获取到东方财富-指数-日频数据 ({symbol}, {period}, {adjust})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_board_industry_hist_em(
                df, 
                symbol=symbol, 
                start_date=start_date, 
                end_date=end_date, 
                period=period, 
                adjust=adjust
            )
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_board_industry_hist_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新东方财富-指数-日频数据失败: {e}")
            raise
    
    async def _refresh_stock_board_industry_cons_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新东方财富-成份股数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "小金属")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取成份股数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_board_industry_cons_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到东方财富-成份股数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_board_industry_cons_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_board_industry_cons_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新东方财富-成份股数据失败: {e}")
            raise


    async def _refresh_stock_comment_detail_zhpj_lspf_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新历史评分数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "600000")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取历史评分数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_comment_detail_zhpj_lspf_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到历史评分数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_comment_detail_zhpj_lspf_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_comment_detail_zhpj_lspf_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新历史评分数据失败: {e}")
            raise


    async def _refresh_stock_comment_detail_scrd_focus_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新用户关注指数数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "600000")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取用户关注指数数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_comment_detail_scrd_focus_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到用户关注指数数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_comment_detail_scrd_focus_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_comment_detail_scrd_focus_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新用户关注指数数据失败: {e}")
            raise


    async def _refresh_stock_comment_detail_scrd_desire_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新市场参与意愿数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "600000")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取市场参与意愿数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_comment_detail_scrd_desire_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到市场参与意愿数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_comment_detail_scrd_desire_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_comment_detail_scrd_desire_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新市场参与意愿数据失败: {e}")
            raise


    async def _refresh_stock_comment_detail_scrd_desire_daily_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新日度市场参与意愿数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            symbol = params.get("symbol", "600000")
            
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在从东方财富获取日度市场参与意愿数据 ({symbol})..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_comment_detail_scrd_desire_daily_em(symbol=symbol)
            
            if df is None or df.empty:
                raise ValueError(f"未获取到日度市场参与意愿数据 ({symbol})")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_comment_detail_scrd_desire_daily_em(df, symbol=symbol)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_comment_detail_scrd_desire_daily_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新日度市场参与意愿数据失败: {e}")
            raise


    async def _refresh_stock_hsgt_fund_flow_summary_em(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新沪深港通资金流向数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从东方财富获取沪深港通资金流向数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_hsgt_fund_flow_summary_em()
            
            if df is None or df.empty:
                raise ValueError("未获取到沪深港通资金流向数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_hsgt_fund_flow_summary_em(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_hsgt_fund_flow_summary_em"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新沪深港通资金流向数据失败: {e}")
            raise


    async def _refresh_stock_sgt_settlement_exchange_rate_szse(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新结算汇率-深港通数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从深交所获取结算汇率-深港通数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sgt_settlement_exchange_rate_szse()
            
            if df is None or df.empty:
                raise ValueError("未获取到结算汇率-深港通数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sgt_settlement_exchange_rate_szse(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sgt_settlement_exchange_rate_szse"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新结算汇率-深港通数据失败: {e}")
            raise


    async def _refresh_stock_sgt_settlement_exchange_rate_sse(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新结算汇率-沪港通数据
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从上交所获取结算汇率-沪港通数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sgt_settlement_exchange_rate_sse()
            
            if df is None or df.empty:
                raise ValueError("未获取到结算汇率-沪港通数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sgt_settlement_exchange_rate_sse(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sgt_settlement_exchange_rate_sse"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新结算汇率-沪港通数据失败: {e}")
            raise

    async def _refresh_stock_sgt_reference_exchange_rate_szse(
        self, 
        task_id: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        刷新参考汇率-深港通数据 (需求107)
        
        Args:
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, "正在从深交所获取参考汇率-深港通数据..."
            )
            
            # 调用provider获取数据
            df = await self.provider.get_stock_sgt_reference_exchange_rate_szse()
            
            if df is None or df.empty:
                raise ValueError("未获取到参考汇率-深港通数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 保存数据
            saved_count = await self.data_service.save_stock_sgt_reference_exchange_rate_szse(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": "stock_sgt_reference_exchange_rate_szse"
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新参考汇率-深港通数据失败: {e}")
            raise

    async def _refresh_stock_sgt_reference_exchange_rate_sse(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新参考汇率-沪港通数据 (需求108)"""
        return await self._generic_refresh(task_id, params, "stock_sgt_reference_exchange_rate_sse", "参考汇率-沪港通")

    async def _refresh_stock_hk_ggt_components_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新港股通成份股数据 (需求109)"""
        return await self._generic_refresh(task_id, params, "stock_hk_ggt_components_em", "港股通成份股")

    async def _refresh_stock_hsgt_fund_min_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新沪深港通分时数据 (需求110)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_fund_min_em", "沪深港通分时")

    async def _refresh_stock_hsgt_board_rank_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新板块排行数据 (需求111)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_board_rank_em", "板块排行", params)

    async def _refresh_stock_hsgt_hold_stock_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新个股排行数据 (需求112)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_hold_stock_em", "个股排行", params)

    async def _refresh_stock_hsgt_stock_statistics_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新每日个股统计数据 (需求113)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_stock_statistics_em", "每日个股统计", params)

    async def _refresh_stock_hsgt_institution_statistics_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新机构排行数据 (需求114)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_institution_statistics_em", "机构排行", params)

    async def _refresh_stock_hsgt_sh_hk_spot_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新沪深港通-港股通(沪>港)实时行情数据 (需求115)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_sh_hk_spot_em", "港股通实时行情")

    async def _refresh_stock_hsgt_hist_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新沪深港通历史数据 (需求116)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_hist_em", "沪深港通历史", params)

    async def _refresh_stock_hsgt_individual_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新沪深港通持股-个股数据 (需求117)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_individual_em", "沪深港通持股-个股", params)

    async def _refresh_stock_hsgt_individual_detail_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新沪深港通持股-个股详情数据 (需求118)"""
        return await self._generic_refresh(task_id, params, "stock_hsgt_individual_detail_em", "沪深港通持股-个股详情", params)

    async def _refresh_stock_em_hsgt_north_net_flow_in(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新北向资金流入数据 (需求119)"""
        return await self._generic_refresh(task_id, params, "stock_em_hsgt_north_net_flow_in", "北向资金流入", params)

    async def _refresh_stock_em_hsgt_south_net_flow_in(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新南向资金流入数据 (需求120)"""
        return await self._generic_refresh(task_id, params, "stock_em_hsgt_south_net_flow_in", "南向资金流入", params)

    async def _refresh_news_trade_notify_dividend_baidu(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新分红派息数据 (需求121)"""
        return await self._generic_refresh(task_id, params, "news_trade_notify_dividend_baidu", "分红派息")

    async def _refresh_stock_news_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新个股新闻数据 (需求122)"""
        return await self._generic_refresh(task_id, params, "stock_news_em", "个股新闻", params)

    async def _refresh_stock_news_main_cx(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财经内容精选数据 (需求123)"""
        return await self._generic_refresh(task_id, params, "stock_news_main_cx", "财经内容精选")

    async def _refresh_news_report_time_baidu(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财报发行数据 (需求124)"""
        return await self._generic_refresh(task_id, params, "news_report_time_baidu", "财报发行")

    async def _refresh_stock_dxsyl_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新打新收益率数据 (需求125)"""
        return await self._generic_refresh(task_id, params, "stock_dxsyl_em", "打新收益率")

    async def _refresh_stock_xgsglb_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新新股申购与中签数据 (需求126)"""
        return await self._generic_refresh(task_id, params, "stock_xgsglb_em", "新股申购与中签")

    async def _refresh_stock_yjbb_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新业绩报表数据 (需求127)"""
        return await self._generic_refresh(task_id, params, "stock_yjbb_em", "业绩报表", params)

    async def _refresh_stock_yjkb_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新业绩快报数据 (需求128)"""
        return await self._generic_refresh(task_id, params, "stock_yjkb_em", "业绩快报", params)

    async def _refresh_stock_yjyg_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新业绩预告数据 (需求129)"""
        return await self._generic_refresh(task_id, params, "stock_yjyg_em", "业绩预告")

    async def _refresh_stock_yysj_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新营业收入数据 (需求130)"""
        return await self._generic_refresh(task_id, params, "stock_yysj_em", "营业收入")

    async def _refresh_stock_report_disclosure(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新报告披露数据 (需求131)"""
        return await self._generic_refresh(task_id, params, "stock_report_disclosure", "报告披露")

    async def _refresh_stock_zh_a_disclosure_report_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新信息披露报告数据 (需求132)"""
        return await self._generic_refresh(task_id, params, "stock_zh_a_disclosure_report_cninfo", "信息披露报告", params)

    async def _refresh_stock_zh_a_disclosure_relation_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新关联方披露数据 (需求133)"""
        return await self._generic_refresh(task_id, params, "stock_zh_a_disclosure_relation_cninfo", "关联方披露", params)

    async def _refresh_stock_industry_category_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新行业分类数据 (需求134)"""
        return await self._generic_refresh(task_id, params, "stock_industry_category_cninfo", "行业分类", params)

    async def _refresh_stock_industry_change_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新行业变更数据 (需求135)"""
        return await self._generic_refresh(task_id, params, "stock_industry_change_cninfo", "行业变更", params)

    async def _refresh_stock_share_change_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新股本变动数据 (需求136)"""
        return await self._generic_refresh(task_id, params, "stock_share_change_cninfo", "股本变动", params)

    async def _refresh_stock_allotment_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新配股数据 (需求137)"""
        return await self._generic_refresh(task_id, params, "stock_allotment_cninfo", "配股", params)

    async def _refresh_stock_profile_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新公司概况数据 (需求138)"""
        return await self._generic_refresh(task_id, params, "stock_profile_cninfo", "公司概况", params)

    async def _refresh_stock_ipo_summary_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新IPO摘要数据 (需求139)"""
        return await self._generic_refresh(task_id, params, "stock_ipo_summary_cninfo", "IPO摘要")

    async def _refresh_stock_ipo_info_cninfo(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新IPO信息数据 (需求140)"""
        return await self._generic_refresh(task_id, params, "stock_ipo_info_cninfo", "IPO信息", params)

    async def _refresh_stock_zcfz_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新资产负债表数据 (需求141)"""
        return await self._generic_refresh(task_id, params, "stock_zcfz_em", "资产负债表", params)

    async def _refresh_stock_lrb_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新利润表数据 (需求142)"""
        return await self._generic_refresh(task_id, params, "stock_lrb_em", "利润表", params)

    async def _refresh_stock_xjll_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现金流量表数据 (需求143)"""
        return await self._generic_refresh(task_id, params, "stock_xjll_em", "现金流量表", params)

    async def _refresh_stock_cwbbzy_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新主要指标数据 (需求144)"""
        return await self._generic_refresh(task_id, params, "stock_cwbbzy_em", "主要指标", params)

    async def _refresh_stock_yjkb_em_v2(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新业绩快报V2数据 (需求145)"""
        return await self._generic_refresh(task_id, params, "stock_yjkb_em_v2", "业绩快报V2", params)

    async def _refresh_stock_profit_forecast_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新盈利预测数据 (需求146)"""
        return await self._generic_refresh(task_id, params, "stock_profit_forecast_em", "盈利预测", params)

    async def _refresh_stock_fhps_detail_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新分红派送详情数据 (需求147)"""
        return await self._generic_refresh(task_id, params, "stock_fhps_detail_ths", "分红派送详情", params)

    async def _refresh_stock_hk_fhpx_detail_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新港股分红派息数据 (需求148)"""
        return await self._generic_refresh(task_id, params, "stock_hk_fhpx_detail_ths", "港股分红派息", params)

    async def _refresh_stock_fund_flow_individual(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新个股资金流向数据 (需求149)"""
        return await self._generic_refresh(task_id, params, "stock_fund_flow_individual", "个股资金流向", params)

    async def _refresh_stock_fund_flow_concept(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新概念资金流向数据 (需求150)"""
        return await self._generic_refresh(task_id, params, "stock_fund_flow_concept", "概念资金流向", params)

    async def _refresh_stock_fund_flow_industry(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新行业资金流向数据 (需求151)"""
        return await self._generic_refresh(task_id, params, "stock_fund_flow_industry", "行业资金流向", params)

    async def _refresh_stock_fund_flow_big_deal(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新大单资金流向数据 (需求152)"""
        return await self._generic_refresh(task_id, params, "stock_fund_flow_big_deal", "大单资金流向", params)

    async def _refresh_stock_individual_fund_flow(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新个股历史资金流向数据 (需求153)"""
        return await self._generic_refresh(task_id, params, "stock_individual_fund_flow", "个股历史资金流向", params)

    async def _refresh_stock_individual_fund_flow_rank(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新个股资金流排名数据 (需求154)"""
        return await self._generic_refresh(task_id, params, "stock_individual_fund_flow_rank", "个股资金流排名", params)

    async def _refresh_stock_market_fund_flow(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新市场资金流向数据 (需求155)"""
        return await self._generic_refresh(task_id, params, "stock_market_fund_flow", "市场资金流向")

    async def _refresh_stock_sector_fund_flow_rank(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新板块资金流排名数据 (需求156)"""
        return await self._generic_refresh(task_id, params, "stock_sector_fund_flow_rank", "板块资金流排名", params)

    async def _refresh_stock_main_fund_flow(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新主力资金流向数据 (需求157)"""
        return await self._generic_refresh(task_id, params, "stock_main_fund_flow", "主力资金流向")

    async def _refresh_stock_sector_fund_flow_summary(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新板块资金流汇总数据 (需求158)"""
        return await self._generic_refresh(task_id, params, "stock_sector_fund_flow_summary", "板块资金流汇总")

    async def _refresh_stock_sector_fund_flow_hist(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新板块历史资金流向数据 (需求159)"""
        return await self._generic_refresh(task_id, params, "stock_sector_fund_flow_hist", "板块历史资金流向", params)

    async def _refresh_stock_concept_fund_flow_hist(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新概念历史资金流向数据 (需求160)"""
        return await self._generic_refresh(task_id, params, "stock_concept_fund_flow_hist", "概念历史资金流向", params)

    async def _refresh_stock_cyq_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新筹码分布数据 (需求161)"""
        return await self._generic_refresh(task_id, params, "stock_cyq_em", "筹码分布", params)

    async def _refresh_stock_gddh_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新股东大会数据 (需求162)"""
        return await self._generic_refresh(task_id, params, "stock_gddh_em", "股东大会", params)

    async def _refresh_stock_zdhtmx_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新重大合同明细数据 (需求163)"""
        return await self._generic_refresh(task_id, params, "stock_zdhtmx_em", "重大合同明细", params)

    async def _refresh_stock_research_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新研究报告数据 (需求164)"""
        return await self._generic_refresh(task_id, params, "stock_research_report_em", "研究报告", params)

    async def _refresh_stock_notice_report(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新公告报告数据 (需求165)"""
        return await self._generic_refresh(task_id, params, "stock_notice_report", "公告报告", params)

    async def _refresh_stock_financial_report_sina(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务报告数据-新浪 (需求166)"""
        return await self._generic_refresh(task_id, params, "stock_financial_report_sina", "财务报告-新浪", params)

    async def _refresh_stock_balance_sheet_by_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新资产负债表-按报告期数据 (需求167)"""
        return await self._generic_refresh(task_id, params, "stock_balance_sheet_by_report_em", "资产负债表-按报告期", params)

    async def _refresh_stock_balance_sheet_by_yearly_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新资产负债表-按年度数据 (需求168)"""
        return await self._generic_refresh(task_id, params, "stock_balance_sheet_by_yearly_em", "资产负债表-按年度", params)

    async def _refresh_stock_profit_sheet_by_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新利润表-按报告期数据 (需求169)"""
        return await self._generic_refresh(task_id, params, "stock_profit_sheet_by_report_em", "利润表-按报告期", params)

    async def _refresh_stock_profit_sheet_by_quarterly_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新利润表-按季度数据 (需求170)"""
        return await self._generic_refresh(task_id, params, "stock_profit_sheet_by_quarterly_em", "利润表-按季度", params)

    async def _refresh_stock_profit_sheet_by_yearly_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新利润表-按年度数据 (需求171)"""
        return await self._generic_refresh(task_id, params, "stock_profit_sheet_by_yearly_em", "利润表-按年度", params)

    async def _refresh_stock_cash_flow_sheet_by_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现金流量表-按报告期数据 (需求172)"""
        return await self._generic_refresh(task_id, params, "stock_cash_flow_sheet_by_report_em", "现金流量表-按报告期", params)

    async def _refresh_stock_cash_flow_sheet_by_yearly_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现金流量表-按年度数据 (需求173)"""
        return await self._generic_refresh(task_id, params, "stock_cash_flow_sheet_by_yearly_em", "现金流量表-按年度", params)

    async def _refresh_stock_cash_flow_sheet_by_quarterly_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现金流量表-按季度数据 (需求174)"""
        return await self._generic_refresh(task_id, params, "stock_cash_flow_sheet_by_quarterly_em", "现金流量表-按季度", params)

    async def _refresh_stock_financial_debt_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务负债数据-同花顺 (需求175)"""
        return await self._generic_refresh(task_id, params, "stock_financial_debt_ths", "财务负债-同花顺", params)

    async def _refresh_stock_financial_benefit_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务收益数据-同花顺 (需求176)"""
        return await self._generic_refresh(task_id, params, "stock_financial_benefit_ths", "财务收益-同花顺", params)

    async def _refresh_stock_financial_cash_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务现金数据-同花顺 (需求177)"""
        return await self._generic_refresh(task_id, params, "stock_financial_cash_ths", "财务现金-同花顺", params)

    async def _refresh_stock_balance_sheet_by_report_delisted_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新退市公司资产负债表数据 (需求178)"""
        return await self._generic_refresh(task_id, params, "stock_balance_sheet_by_report_delisted_em", "退市公司资产负债表", params)

    async def _refresh_stock_profit_sheet_by_report_delisted_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新退市公司利润表数据 (需求179)"""
        return await self._generic_refresh(task_id, params, "stock_profit_sheet_by_report_delisted_em", "退市公司利润表", params)

    async def _refresh_stock_cash_flow_sheet_by_report_delisted_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新退市公司现金流量表数据 (需求180)"""
        return await self._generic_refresh(task_id, params, "stock_cash_flow_sheet_by_report_delisted_em", "退市公司现金流量表", params)

    async def _refresh_stock_financial_hk_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新港股财务报告数据 (需求181)"""
        return await self._generic_refresh(task_id, params, "stock_financial_hk_report_em", "港股财务报告", params)

    async def _refresh_stock_financial_us_report_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新美股财务报告数据 (需求182)"""
        return await self._generic_refresh(task_id, params, "stock_financial_us_report_em", "美股财务报告", params)

    async def _refresh_stock_financial_abstract(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务摘要数据 (需求183)"""
        return await self._generic_refresh(task_id, params, "stock_financial_abstract", "财务摘要", params)

    async def _refresh_stock_financial_abstract_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务摘要数据-同花顺 (需求184)"""
        return await self._generic_refresh(task_id, params, "stock_financial_abstract_ths", "财务摘要-同花顺", params)

    async def _refresh_stock_financial_analysis_indicator_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务分析指标数据 (需求185)"""
        return await self._generic_refresh(task_id, params, "stock_financial_analysis_indicator_em", "财务分析指标", params)

    async def _refresh_stock_financial_analysis_indicator(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新财务分析指标数据-新浪 (需求186)"""
        return await self._generic_refresh(task_id, params, "stock_financial_analysis_indicator", "财务分析指标-新浪", params)

    async def _refresh_stock_financial_hk_analysis_indicator_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新港股财务分析指标数据 (需求187)"""
        return await self._generic_refresh(task_id, params, "stock_financial_hk_analysis_indicator_em", "港股财务分析指标", params)

    async def _refresh_stock_financial_us_analysis_indicator_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新美股财务分析指标数据 (需求188)"""
        return await self._generic_refresh(task_id, params, "stock_financial_us_analysis_indicator_em", "美股财务分析指标", params)

    async def _refresh_stock_history_dividend(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新历史分红数据 (需求189)"""
        return await self._generic_refresh(task_id, params, "stock_history_dividend", "历史分红")

    async def _refresh_stock_gdfx_free_top_10_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新前10大流通股东数据 (需求190)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_free_top_10_em", "前10大流通股东", params)

    async def _refresh_stock_gdfx_top_10_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新前10大股东数据 (需求191)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_top_10_em", "前10大股东", params)

    async def _refresh_stock_gdfx_free_holding_change_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新流通股东持股变化数据 (需求192)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_free_holding_change_em", "流通股东持股变化", params)

    async def _refresh_stock_gdfx_holding_change_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新股东持股变化数据 (需求193)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_holding_change_em", "股东持股变化", params)

    async def _refresh_stock_management_change_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新高管变动数据 (需求194)"""
        return await self._generic_refresh(task_id, params, "stock_management_change_ths", "高管变动", params)

    async def _refresh_stock_shareholder_change_ths(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新股东变动数据 (需求195)"""
        return await self._generic_refresh(task_id, params, "stock_shareholder_change_ths", "股东变动", params)

    async def _refresh_stock_gdfx_free_holding_analyse_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新流通股东持股分析数据 (需求196)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_free_holding_analyse_em", "流通股东持股分析", params)

    async def _refresh_stock_gdfx_holding_analyse_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新股东持股分析数据 (需求197)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_holding_analyse_em", "股东持股分析", params)

    async def _refresh_stock_gdfx_free_holding_detail_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新流通股东持股明细数据 (需求198)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_free_holding_detail_em", "流通股东持股明细", params)

    async def _refresh_stock_gdfx_holding_detail_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新股东持股明细数据 (需求199)"""
        return await self._generic_refresh(task_id, params, "stock_gdfx_holding_detail_em", "股东持股明细", params)

    async def _refresh_stock_history_dividend_detail(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新历史分红详细数据 (需求200)"""
        return await self._generic_refresh(task_id, params, "stock_history_dividend_detail", "历史分红详细", params)

    async def _generic_refresh(
        self, 
        task_id: str, 
        params: Dict[str, Any],
        collection_name: str,
        display_name: str,
        provider_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        通用刷新方法模板
        
        Args:
            task_id: 任务ID
            params: 刷新参数
            collection_name: 集合名称
            display_name: 显示名称
            provider_params: Provider方法参数
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, f"正在获取{display_name}数据..."
            )
            
            # 获取provider方法
            provider_method = getattr(self.provider, f"get_{collection_name}")
            
            # 调用provider获取数据
            if provider_params:
                df = await provider_method(**provider_params)
            else:
                df = await provider_method()
            
            if df is None or df.empty:
                raise ValueError(f"未获取到{display_name}数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(df)} 条数据...")
            
            # 获取data_service方法
            save_method = getattr(self.data_service, f"save_{collection_name}")
            
            # 保存数据
            saved_count = await save_method(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved_count} 条数据")
            
            return {
                "saved": saved_count,
                "total": len(df),
                "collection": collection_name
            }
            
        except Exception as e:
            logger.error(f"❌ 刷新{display_name}数据失败: {e}")
            raise

    # TODO: 需求121-200的刷新方法可以继续使用_generic_refresh模板实现


# 全局服务实例
_stock_refresh_service = None


def get_stock_refresh_service() -> StockRefreshService:
    """获取股票刷新服务实例"""
    global _stock_refresh_service
    if _stock_refresh_service is None:
        _stock_refresh_service = StockRefreshService()
    return _stock_refresh_service
