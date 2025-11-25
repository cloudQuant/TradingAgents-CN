"""
基金数据刷新服务 V2
重构版：使用funds目录中的provider和service模块
"""
import logging
from typing import Dict, Any
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager

# 导入所有基金服务
from app.services.data_sources.funds.services.fund_name_em_service import FundNameEmService
from app.services.data_sources.funds.services.fund_basic_info_service import FundBasicInfoService
from app.services.data_sources.funds.services.fund_info_index_em_service import FundInfoIndexEmService
from app.services.data_sources.funds.services.fund_purchase_status_service import FundPurchaseStatusService
from app.services.data_sources.funds.services.fund_etf_spot_em_service import FundEtfSpotEmService
from app.services.data_sources.funds.services.fund_etf_spot_ths_service import FundEtfSpotThsService
from app.services.data_sources.funds.services.fund_lof_spot_em_service import FundLofSpotEmService
from app.services.data_sources.funds.services.fund_spot_sina_service import FundSpotSinaService
from app.services.data_sources.funds.services.fund_etf_hist_min_em_service import FundEtfHistMinEmService
from app.services.data_sources.funds.services.fund_lof_hist_min_em_service import FundLofHistMinEmService
from app.services.data_sources.funds.services.fund_etf_hist_em_service import FundEtfHistEmService
from app.services.data_sources.funds.services.fund_lof_hist_em_service import FundLofHistEmService
from app.services.data_sources.funds.services.fund_hist_sina_service import FundHistSinaService
from app.services.data_sources.funds.services.fund_open_fund_daily_em_service import FundOpenFundDailyEmService
from app.services.data_sources.funds.services.fund_open_fund_info_em_service import FundOpenFundInfoEmService
from app.services.data_sources.funds.services.fund_money_fund_daily_em_service import FundMoneyFundDailyEmService
from app.services.data_sources.funds.services.fund_money_fund_info_em_service import FundMoneyFundInfoEmService
from app.services.data_sources.funds.services.fund_financial_fund_daily_em_service import FundFinancialFundDailyEmService
from app.services.data_sources.funds.services.fund_financial_fund_info_em_service import FundFinancialFundInfoEmService
from app.services.data_sources.funds.services.fund_graded_fund_daily_em_service import FundGradedFundDailyEmService
from app.services.data_sources.funds.services.fund_graded_fund_info_em_service import FundGradedFundInfoEmService
from app.services.data_sources.funds.services.fund_etf_fund_daily_em_service import FundEtfFundDailyEmService
from app.services.data_sources.funds.services.fund_hk_hist_em_service import FundHkHistEmService
from app.services.data_sources.funds.services.fund_etf_fund_info_em_service import FundEtfFundInfoEmService
from app.services.data_sources.funds.services.fund_etf_dividend_sina_service import FundEtfDividendSinaService
from app.services.data_sources.funds.services.fund_fh_em_service import FundFhEmService
from app.services.data_sources.funds.services.fund_cf_em_service import FundCfEmService
from app.services.data_sources.funds.services.fund_fh_rank_em_service import FundFhRankEmService
from app.services.data_sources.funds.services.fund_open_fund_rank_em_service import FundOpenFundRankEmService
from app.services.data_sources.funds.services.fund_exchange_rank_em_service import FundExchangeRankEmService
from app.services.data_sources.funds.services.fund_money_rank_em_service import FundMoneyRankEmService

logger = logging.getLogger("webapi")


class FundRefreshServiceV2:
    """基金数据刷新服务 V2"""
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        
        # 初始化所有服务
        self.services = {
            "fund_name_em": FundNameEmService(self.db),
            "fund_basic_info": FundBasicInfoService(self.db),
            "fund_info_index_em": FundInfoIndexEmService(self.db),
            "fund_purchase_status": FundPurchaseStatusService(self.db),
            "fund_etf_spot_em": FundEtfSpotEmService(self.db),
            "fund_etf_spot_ths": FundEtfSpotThsService(self.db),
            "fund_lof_spot_em": FundLofSpotEmService(self.db),
            "fund_spot_sina": FundSpotSinaService(self.db),
            "fund_etf_hist_min_em": FundEtfHistMinEmService(self.db),
            "fund_lof_hist_min_em": FundLofHistMinEmService(self.db),
            "fund_etf_hist_em": FundEtfHistEmService(self.db),
            "fund_lof_hist_em": FundLofHistEmService(self.db),
            "fund_hist_sina": FundHistSinaService(self.db),
            "fund_open_fund_daily_em": FundOpenFundDailyEmService(self.db),
            "fund_open_fund_info_em": FundOpenFundInfoEmService(self.db),
            "fund_money_fund_daily_em": FundMoneyFundDailyEmService(self.db),
            "fund_money_fund_info_em": FundMoneyFundInfoEmService(self.db),
            "fund_financial_fund_daily_em": FundFinancialFundDailyEmService(self.db),
            "fund_financial_fund_info_em": FundFinancialFundInfoEmService(self.db),
            "fund_graded_fund_daily_em": FundGradedFundDailyEmService(self.db),
            "fund_graded_fund_info_em": FundGradedFundInfoEmService(self.db),
            "fund_etf_fund_daily_em": FundEtfFundDailyEmService(self.db),
            "fund_hk_hist_em": FundHkHistEmService(self.db),
            "fund_etf_fund_info_em": FundEtfFundInfoEmService(self.db),
            "fund_etf_dividend_sina": FundEtfDividendSinaService(self.db),
            "fund_fh_em": FundFhEmService(self.db),
            "fund_cf_em": FundCfEmService(self.db),
            "fund_fh_rank_em": FundFhRankEmService(self.db),
            "fund_open_fund_rank_em": FundOpenFundRankEmService(self.db),
            "fund_exchange_rank_em": FundExchangeRankEmService(self.db),
            "fund_money_rank_em": FundMoneyRankEmService(self.db),
        }
    
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
            
            # 检查服务是否存在
            if collection_name not in self.services:
                raise ValueError(f"未找到集合 {collection_name} 的服务")
            
            service = self.services[collection_name]
            
            # 更新进度
            self.task_manager.update_progress(task_id, 10, 100, f"正在获取 {collection_name} 数据...")
            
            # 调用服务刷新数据
            result = await service.refresh_data(**(params or {}))
            
            if result.get("success"):
                self.task_manager.update_progress(
                    task_id, 100, 100, 
                    f"成功刷新 {collection_name}，插入 {result.get('inserted', 0)} 条数据"
                )
                self.task_manager.complete_task(task_id)
            else:
                self.task_manager.fail_task(task_id, result.get("message", "刷新失败"))
            
            return result
            
        except Exception as e:
            logger.error(f"刷新 {collection_name} 失败: {e}", exc_info=True)
            self.task_manager.fail_task(task_id, str(e))
            raise
    
    async def get_collection_overview(self, collection_name: str) -> Dict[str, Any]:
        """获取集合数据概览"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        service = self.services[collection_name]
        return await service.get_overview()
    
    async def get_collection_data(
        self,
        collection_name: str,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None
    ) -> Dict[str, Any]:
        """获取集合数据"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        service = self.services[collection_name]
        return await service.get_data(skip=skip, limit=limit, filters=filters)
    
    async def clear_collection(self, collection_name: str) -> Dict[str, Any]:
        """清空集合数据"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        service = self.services[collection_name]
        return await service.clear_data()
