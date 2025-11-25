"""
期货数据刷新服务
重构版：使用futures目录中的provider和service模块
包含全部52个期货数据集合
"""
import logging
from typing import Dict, Any
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager

# 导入所有期货服务
from app.services.data_sources.futures.services.futures_fees_info_service import FuturesFeesInfoService
from app.services.data_sources.futures.services.futures_comm_info_service import FuturesCommInfoService
from app.services.data_sources.futures.services.futures_rule_service import FuturesRuleService
from app.services.data_sources.futures.services.futures_inventory_99_service import FuturesInventory99Service
from app.services.data_sources.futures.services.futures_inventory_em_service import FuturesInventoryEmService
from app.services.data_sources.futures.services.futures_dce_position_rank_service import FuturesDcePositionRankService
from app.services.data_sources.futures.services.futures_gfex_position_rank_service import FuturesGfexPositionRankService
from app.services.data_sources.futures.services.futures_warehouse_receipt_czce_service import FuturesWarehouseReceiptCzceService
from app.services.data_sources.futures.services.futures_warehouse_receipt_dce_service import FuturesWarehouseReceiptDceService
from app.services.data_sources.futures.services.futures_shfe_warehouse_receipt_service import FuturesShfeWarehouseReceiptService
from app.services.data_sources.futures.services.futures_gfex_warehouse_receipt_service import FuturesGfexWarehouseReceiptService
from app.services.data_sources.futures.services.futures_to_spot_dce_service import FuturesToSpotDceService
from app.services.data_sources.futures.services.futures_to_spot_czce_service import FuturesToSpotCzceService
from app.services.data_sources.futures.services.futures_to_spot_shfe_service import FuturesToSpotShfeService
from app.services.data_sources.futures.services.futures_spot_sys_service import FuturesSpotSysService
from app.services.data_sources.futures.services.futures_contract_info_shfe_service import FuturesContractInfoShfeService
from app.services.data_sources.futures.services.futures_contract_info_ine_service import FuturesContractInfoIneService
from app.services.data_sources.futures.services.futures_contract_info_dce_service import FuturesContractInfoDceService
from app.services.data_sources.futures.services.futures_contract_info_czce_service import FuturesContractInfoCzceService
from app.services.data_sources.futures.services.futures_contract_info_gfex_service import FuturesContractInfoGfexService
from app.services.data_sources.futures.services.futures_contract_info_cffex_service import FuturesContractInfoCffexService
from app.services.data_sources.futures.services.futures_zh_spot_service import FuturesZhSpotService
from app.services.data_sources.futures.services.futures_zh_realtime_service import FuturesZhRealtimeService
from app.services.data_sources.futures.services.futures_zh_minute_sina_service import FuturesZhMinuteSinaService
from app.services.data_sources.futures.services.futures_hist_em_service import FuturesHistEmService
from app.services.data_sources.futures.services.futures_zh_daily_sina_service import FuturesZhDailySinaService
from app.services.data_sources.futures.services.get_futures_daily_service import GetFuturesDailyService
from app.services.data_sources.futures.services.futures_hq_subscribe_exchange_symbol_service import FuturesHqSubscribeExchangeSymbolService
from app.services.data_sources.futures.services.futures_foreign_commodity_realtime_service import FuturesForeignCommodityRealtimeService
from app.services.data_sources.futures.services.futures_global_spot_em_service import FuturesGlobalSpotEmService
from app.services.data_sources.futures.services.futures_global_hist_em_service import FuturesGlobalHistEmService
from app.services.data_sources.futures.services.futures_foreign_hist_service import FuturesForeignHistService
from app.services.data_sources.futures.services.futures_foreign_detail_service import FuturesForeignDetailService
from app.services.data_sources.futures.services.futures_settlement_price_sgx_service import FuturesSettlementPriceSgxService
from app.services.data_sources.futures.services.futures_main_sina_service import FuturesMainSinaService
from app.services.data_sources.futures.services.futures_contract_detail_service import FuturesContractDetailService
from app.services.data_sources.futures.services.futures_contract_detail_em_service import FuturesContractDetailEmService
from app.services.data_sources.futures.services.futures_index_ccidx_service import FuturesIndexCcidxService
from app.services.data_sources.futures.services.futures_spot_stock_service import FuturesSpotStockService
from app.services.data_sources.futures.services.futures_comex_inventory_service import FuturesComexInventoryService
from app.services.data_sources.futures.services.futures_hog_core_service import FuturesHogCoreService
from app.services.data_sources.futures.services.futures_hog_cost_service import FuturesHogCostService
from app.services.data_sources.futures.services.futures_hog_supply_service import FuturesHogSupplyService
from app.services.data_sources.futures.services.index_hog_spot_price_service import IndexHogSpotPriceService
from app.services.data_sources.futures.services.futures_news_shmet_service import FuturesNewsShmetService

logger = logging.getLogger("webapi")


class FuturesRefreshService:
    """期货数据刷新服务"""
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        
        # 初始化所有服务
        self.services = {
            "futures_fees_info": FuturesFeesInfoService(self.db),
            "futures_comm_info": FuturesCommInfoService(self.db),
            "futures_rule": FuturesRuleService(self.db),
            "futures_inventory_99": FuturesInventory99Service(self.db),
            "futures_inventory_em": FuturesInventoryEmService(self.db),
            "futures_dce_position_rank": FuturesDcePositionRankService(self.db),
            "futures_gfex_position_rank": FuturesGfexPositionRankService(self.db),
            "futures_warehouse_receipt_czce": FuturesWarehouseReceiptCzceService(self.db),
            "futures_warehouse_receipt_dce": FuturesWarehouseReceiptDceService(self.db),
            "futures_shfe_warehouse_receipt": FuturesShfeWarehouseReceiptService(self.db),
            "futures_gfex_warehouse_receipt": FuturesGfexWarehouseReceiptService(self.db),
            "futures_to_spot_dce": FuturesToSpotDceService(self.db),
            "futures_to_spot_czce": FuturesToSpotCzceService(self.db),
            "futures_to_spot_shfe": FuturesToSpotShfeService(self.db),
            "futures_spot_sys": FuturesSpotSysService(self.db),
            "futures_contract_info_shfe": FuturesContractInfoShfeService(self.db),
            "futures_contract_info_ine": FuturesContractInfoIneService(self.db),
            "futures_contract_info_dce": FuturesContractInfoDceService(self.db),
            "futures_contract_info_czce": FuturesContractInfoCzceService(self.db),
            "futures_contract_info_gfex": FuturesContractInfoGfexService(self.db),
            "futures_contract_info_cffex": FuturesContractInfoCffexService(self.db),
            "futures_zh_spot": FuturesZhSpotService(self.db),
            "futures_zh_realtime": FuturesZhRealtimeService(self.db),
            "futures_zh_minute_sina": FuturesZhMinuteSinaService(self.db),
            "futures_hist_em": FuturesHistEmService(self.db),
            "futures_zh_daily_sina": FuturesZhDailySinaService(self.db),
            "get_futures_daily": GetFuturesDailyService(self.db),
            "futures_hq_subscribe_exchange_symbol": FuturesHqSubscribeExchangeSymbolService(self.db),
            "futures_foreign_commodity_realtime": FuturesForeignCommodityRealtimeService(self.db),
            "futures_global_spot_em": FuturesGlobalSpotEmService(self.db),
            "futures_global_hist_em": FuturesGlobalHistEmService(self.db),
            "futures_foreign_hist": FuturesForeignHistService(self.db),
            "futures_foreign_detail": FuturesForeignDetailService(self.db),
            "futures_settlement_price_sgx": FuturesSettlementPriceSgxService(self.db),
            "futures_main_sina": FuturesMainSinaService(self.db),
            "futures_contract_detail": FuturesContractDetailService(self.db),
            "futures_contract_detail_em": FuturesContractDetailEmService(self.db),
            "futures_index_ccidx": FuturesIndexCcidxService(self.db),
            "futures_spot_stock": FuturesSpotStockService(self.db),
            "futures_comex_inventory": FuturesComexInventoryService(self.db),
            "futures_hog_core": FuturesHogCoreService(self.db),
            "futures_hog_cost": FuturesHogCostService(self.db),
            "futures_hog_supply": FuturesHogSupplyService(self.db),
            "index_hog_spot_price": IndexHogSpotPriceService(self.db),
            "futures_news_shmet": FuturesNewsShmetService(self.db),
        }
    
    # 前端特有的参数，不应传递给 akshare 函数
    FRONTEND_ONLY_PARAMS = {
        'batch', 'batch_update', 'batch_size', 'concurrency', 'delay', 'update_type',
        'page', 'limit', 'skip', 'filters', 'sort', 'order',
        'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
        'force', 'clear_first', 'overwrite', 'mode'
    }
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的期货数据集合
        
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
            
            # 过滤掉前端特有的参数
            api_params = {}
            if params:
                api_params = {
                    k: v for k, v in params.items() 
                    if k not in self.FRONTEND_ONLY_PARAMS
                }
                if is_batch and "concurrency" in params:
                    api_params["concurrency"] = params["concurrency"]
                logger.info(f"[参数过滤] 原始参数: {params}, 过滤后: {api_params}, 批量更新: {is_batch}")
            
            # 调用服务刷新数据
            if is_batch and hasattr(service, "update_batch_data"):
                logger.info(f"[{collection_name}] 调用批量更新方法 update_batch_data")
                result = await service.update_batch_data(task_id=task_id, **api_params)
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
