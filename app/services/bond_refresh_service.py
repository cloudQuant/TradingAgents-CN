"""
债券数据刷新服务
重构版：使用bonds目录中的provider和service模块
包含全部34个债券数据集合
"""
import logging
from typing import Dict, Any
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager

logger = logging.getLogger("webapi")


class BondRefreshService:
    """债券数据刷新服务"""
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        self._services = None  # 延迟初始化
    
    def _init_services(self):
        """延迟初始化所有34个服务"""
        if self._services is not None:
            return
            
        # 导入所有债券服务
        from app.services.data_sources.bonds.services.bond_info_cm_service import BondInfoCmService
        from app.services.data_sources.bonds.services.bond_info_detail_cm_service import BondInfoDetailCmService
        from app.services.data_sources.bonds.services.bond_zh_hs_spot_service import BondZhHsSpotService
        from app.services.data_sources.bonds.services.bond_zh_hs_daily_service import BondZhHsDailyService
        from app.services.data_sources.bonds.services.bond_zh_hs_cov_spot_service import BondZhHsCovSpotService
        from app.services.data_sources.bonds.services.bond_zh_hs_cov_daily_service import BondZhHsCovDailyService
        from app.services.data_sources.bonds.services.bond_zh_cov_service import BondZhCovService
        from app.services.data_sources.bonds.services.bond_cash_summary_sse_service import BondCashSummarySseService
        from app.services.data_sources.bonds.services.bond_deal_summary_sse_service import BondDealSummarySseService
        from app.services.data_sources.bonds.services.bond_debt_nafmii_service import BondDebtNafmiiService
        from app.services.data_sources.bonds.services.bond_spot_quote_service import BondSpotQuoteService
        from app.services.data_sources.bonds.services.bond_spot_deal_service import BondSpotDealService
        from app.services.data_sources.bonds.services.bond_zh_hs_cov_min_service import BondZhHsCovMinService
        from app.services.data_sources.bonds.services.bond_zh_hs_cov_pre_min_service import BondZhHsCovPreMinService
        from app.services.data_sources.bonds.services.bond_zh_cov_info_service import BondZhCovInfoService
        from app.services.data_sources.bonds.services.bond_zh_cov_info_ths_service import BondZhCovInfoThsService
        from app.services.data_sources.bonds.services.bond_cov_comparison_service import BondCovComparisonService
        from app.services.data_sources.bonds.services.bond_zh_cov_value_analysis_service import BondZhCovValueAnalysisService
        from app.services.data_sources.bonds.services.bond_sh_buy_back_em_service import BondShBuyBackEmService
        from app.services.data_sources.bonds.services.bond_sz_buy_back_em_service import BondSzBuyBackEmService
        from app.services.data_sources.bonds.services.bond_buy_back_hist_em_service import BondBuyBackHistEmService
        from app.services.data_sources.bonds.services.bond_cb_jsl_service import BondCbJslService
        from app.services.data_sources.bonds.services.bond_cb_redeem_jsl_service import BondCbRedeemJslService
        from app.services.data_sources.bonds.services.bond_cb_index_jsl_service import BondCbIndexJslService
        from app.services.data_sources.bonds.services.bond_cb_adj_logs_jsl_service import BondCbAdjLogsJslService
        from app.services.data_sources.bonds.services.bond_china_close_return_service import BondChinaCloseReturnService
        from app.services.data_sources.bonds.services.bond_zh_us_rate_service import BondZhUsRateService
        from app.services.data_sources.bonds.services.bond_treasure_issue_cninfo_service import BondTreasureIssueCninfoService
        from app.services.data_sources.bonds.services.bond_local_government_issue_cninfo_service import BondLocalGovernmentIssueCninfoService
        from app.services.data_sources.bonds.services.bond_corporate_issue_cninfo_service import BondCorporateIssueCninfoService
        from app.services.data_sources.bonds.services.bond_cov_issue_cninfo_service import BondCovIssueCninfoService
        from app.services.data_sources.bonds.services.bond_cov_stock_issue_cninfo_service import BondCovStockIssueCninfoService
        from app.services.data_sources.bonds.services.bond_new_composite_index_cbond_service import BondNewCompositeIndexCbondService
        from app.services.data_sources.bonds.services.bond_composite_index_cbond_service import BondCompositeIndexCbondService
        
        # 初始化所有34个服务
        self._services = {
            # 01-02 基础数据
            "bond_info_cm": BondInfoCmService(self.db),
            "bond_info_detail_cm": BondInfoDetailCmService(self.db),
            # 03-04 沪深债券行情
            "bond_zh_hs_spot": BondZhHsSpotService(self.db),
            "bond_zh_hs_daily": BondZhHsDailyService(self.db),
            # 05-07 可转债行情
            "bond_zh_hs_cov_spot": BondZhHsCovSpotService(self.db),
            "bond_zh_hs_cov_daily": BondZhHsCovDailyService(self.db),
            "bond_zh_cov": BondZhCovService(self.db),
            # 08-09 市场概览
            "bond_cash_summary_sse": BondCashSummarySseService(self.db),
            "bond_deal_summary_sse": BondDealSummarySseService(self.db),
            # 10-12 银行间市场
            "bond_debt_nafmii": BondDebtNafmiiService(self.db),
            "bond_spot_quote": BondSpotQuoteService(self.db),
            "bond_spot_deal": BondSpotDealService(self.db),
            # 13-14 可转债分时
            "bond_zh_hs_cov_min": BondZhHsCovMinService(self.db),
            "bond_zh_hs_cov_pre_min": BondZhHsCovPreMinService(self.db),
            # 15-18 可转债详细
            "bond_zh_cov_info": BondZhCovInfoService(self.db),
            "bond_zh_cov_info_ths": BondZhCovInfoThsService(self.db),
            "bond_cov_comparison": BondCovComparisonService(self.db),
            "bond_zh_cov_value_analysis": BondZhCovValueAnalysisService(self.db),
            # 19-21 质押式回购
            "bond_sh_buy_back_em": BondShBuyBackEmService(self.db),
            "bond_sz_buy_back_em": BondSzBuyBackEmService(self.db),
            "bond_buy_back_hist_em": BondBuyBackHistEmService(self.db),
            # 22-25 集思录数据
            "bond_cb_jsl": BondCbJslService(self.db),
            "bond_cb_redeem_jsl": BondCbRedeemJslService(self.db),
            "bond_cb_index_jsl": BondCbIndexJslService(self.db),
            "bond_cb_adj_logs_jsl": BondCbAdjLogsJslService(self.db),
            # 26-27 收益率曲线
            "bond_china_close_return": BondChinaCloseReturnService(self.db),
            "bond_zh_us_rate": BondZhUsRateService(self.db),
            # 28-32 债券发行
            "bond_treasure_issue_cninfo": BondTreasureIssueCninfoService(self.db),
            "bond_local_government_issue_cninfo": BondLocalGovernmentIssueCninfoService(self.db),
            "bond_corporate_issue_cninfo": BondCorporateIssueCninfoService(self.db),
            "bond_cov_issue_cninfo": BondCovIssueCninfoService(self.db),
            "bond_cov_stock_issue_cninfo": BondCovStockIssueCninfoService(self.db),
            # 33-34 中债指数
            "bond_new_composite_index_cbond": BondNewCompositeIndexCbondService(self.db),
            "bond_composite_index_cbond": BondCompositeIndexCbondService(self.db),
        }
    
    @property
    def services(self):
        """获取服务字典（延迟初始化）"""
        if self._services is None:
            self._init_services()
        return self._services
    
    # 前端特有的参数，不应传递给 akshare 函数
    FRONTEND_ONLY_PARAMS = {
        # 批量更新控制参数
        'batch', 'batch_update', 'batch_size', 'concurrency', 'delay', 'update_type',
        # 分页和过滤参数
        'page', 'limit', 'skip', 'filters', 'sort', 'order',
        # 任务和回调参数
        'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
        # 更新控制参数
        'force', 'clear_first', 'overwrite', 'mode'
    }
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的债券数据集合
        
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
            
            # 判断是批量更新还是单条更新
            is_batch = (
                params.get("batch") or 
                params.get("batch_update") or 
                params.get("update_type") == "batch"
            ) if params else False
            
            # 过滤掉前端特有的参数，只保留 akshare 需要的参数
            api_params = {}
            if params:
                api_params = {
                    k: v for k, v in params.items() 
                    if k not in self.FRONTEND_ONLY_PARAMS
                }
                # 对于批量更新，保留 concurrency 参数
                if is_batch and "concurrency" in params:
                    api_params["concurrency"] = params["concurrency"]
                logger.info(f"[参数过滤] 原始参数: {params}, 过滤后: {api_params}, 批量更新: {is_batch}")
            
            # 调用服务刷新数据
            if is_batch and hasattr(service, "update_batch_data"):
                logger.info(f"[{collection_name}] 调用批量更新方法 update_batch_data")
                # 批量更新方法自己管理任务状态和进度
                result = await service.update_batch_data(task_id=task_id, **api_params)
                # 批量更新方法已经处理了任务完成状态，不需要再次调用
            else:
                logger.info(f"[{collection_name}] 调用单条更新方法 update_single_data")
                result = await service.update_single_data(**api_params)
                
                # 单条更新需要在这里处理任务状态
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
    
    def get_supported_collections(self) -> list:
        """获取支持的所有数据集合列表"""
        return list(self.services.keys())
    
    def get_collection_count(self) -> int:
        """获取支持的数据集合数量"""
        return len(self.services)
