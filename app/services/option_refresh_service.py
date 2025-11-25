"""
期权数据刷新服务
负责调度各个期权数据集合的更新任务
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config.option_update_config import OPTION_UPDATE_CONFIGS, get_collection_config

logger = logging.getLogger(__name__)


class OptionRefreshService:
    """期权数据刷新服务"""
    
    def __init__(self, db: AsyncIOMotorDatabase, task_manager=None):
        self.db = db
        self.task_manager = task_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 服务实例缓存
        self._services: Dict[str, Any] = {}
        
        # 延迟导入服务以避免循环导入
        self._service_classes: Dict[str, str] = {}
        self._init_service_mapping()
    
    def _init_service_mapping(self):
        """初始化服务映射"""
        # 映射集合名到服务类路径
        # 格式: collection_name -> (module_path, class_name)
        service_mappings = {
            # 无参数集合
            "option_contract_info_ctp": ("app.services.data_sources.options.services.option_contract_info_ctp_service", "OptionContractInfoCtpService"),
            "option_current_day_sse": ("app.services.data_sources.options.services.option_current_day_sse_service", "OptionCurrentDaySseService"),
            "option_current_day_szse": ("app.services.data_sources.options.services.option_current_day_szse_service", "OptionCurrentDaySzseService"),
            "option_cffex_sz50_list_sina": ("app.services.data_sources.options.services.option_cffex_list_sina_service", "OptionCffexSz50ListSinaService"),
            "option_cffex_hs300_list_sina": ("app.services.data_sources.options.services.option_cffex_list_sina_service", "OptionCffexHs300ListSinaService"),
            "option_cffex_zz1000_list_sina": ("app.services.data_sources.options.services.option_cffex_list_sina_service", "OptionCffexZz1000ListSinaService"),
            "option_current_em": ("app.services.data_sources.options.services.option_em_service", "OptionCurrentEmService"),
            "option_lhb_em": ("app.services.data_sources.options.services.option_em_service", "OptionLhbEmService"),
            "option_value_analysis_em": ("app.services.data_sources.options.services.option_em_service", "OptionValueAnalysisEmService"),
            "option_risk_analysis_em": ("app.services.data_sources.options.services.option_em_service", "OptionRiskAnalysisEmService"),
            "option_premium_analysis_em": ("app.services.data_sources.options.services.option_em_service", "OptionPremiumAnalysisEmService"),
            "option_comm_info": ("app.services.data_sources.options.services.option_misc_service", "OptionCommInfoService"),
            "option_margin": ("app.services.data_sources.options.services.option_misc_service", "OptionMarginService"),
            "option_vol_gfex": ("app.services.data_sources.options.services.option_misc_service", "OptionVolGfexService"),
            
            # 日期参数集合
            "option_risk_indicator_sse": ("app.services.data_sources.options.services.option_sse_service", "OptionRiskIndicatorSseService"),
            "option_daily_stats_sse": ("app.services.data_sources.options.services.option_sse_service", "OptionDailyStatsSseService"),
            "option_daily_stats_szse": ("app.services.data_sources.options.services.option_szse_service", "OptionDailyStatsSzseService"),
            "option_czce_hist": ("app.services.data_sources.options.services.option_exchange_service", "OptionCzceHistService"),
            
            # 品种参数集合
            "option_finance_board": ("app.services.data_sources.options.services.option_finance_service", "OptionFinanceBoardService"),
            "option_cffex_sz50_spot_sina": ("app.services.data_sources.options.services.option_cffex_sina_service", "OptionCffexSz50SpotSinaService"),
            "option_cffex_hs300_spot_sina": ("app.services.data_sources.options.services.option_cffex_sina_service", "OptionCffexHs300SpotSinaService"),
            "option_cffex_zz1000_spot_sina": ("app.services.data_sources.options.services.option_cffex_sina_service", "OptionCffexZz1000SpotSinaService"),
            "option_cffex_sz50_daily_sina": ("app.services.data_sources.options.services.option_cffex_sina_service", "OptionCffexSz50DailySinaService"),
            "option_cffex_hs300_daily_sina": ("app.services.data_sources.options.services.option_cffex_sina_service", "OptionCffexHs300DailySinaService"),
            "option_cffex_zz1000_daily_sina": ("app.services.data_sources.options.services.option_cffex_sina_service", "OptionCffexZz1000DailySinaService"),
            "option_sse_list_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseListSinaService"),
            "option_sse_expire_day_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseExpireDaySinaService"),
            "option_sse_codes_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseCodesSinaService"),
            "option_sse_underlying_spot_price_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseUnderlyingSpotPriceSinaService"),
            "option_sse_greeks_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseGreeksSinaService"),
            "option_sse_minute_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseMinuteSinaService"),
            "option_sse_daily_sina": ("app.services.data_sources.options.services.option_sse_sina_service", "OptionSseDailySinaService"),
            "option_finance_minute_sina": ("app.services.data_sources.options.services.option_finance_sina_service", "OptionFinanceMinuteSinaService"),
            "option_minute_em": ("app.services.data_sources.options.services.option_em_service", "OptionMinuteEmService"),
            "option_commodity_contract_sina": ("app.services.data_sources.options.services.option_commodity_sina_service", "OptionCommodityContractSinaService"),
            "option_commodity_contract_table_sina": ("app.services.data_sources.options.services.option_commodity_sina_service", "OptionCommodityContractTableSinaService"),
            "option_commodity_hist_sina": ("app.services.data_sources.options.services.option_commodity_sina_service", "OptionCommodityHistSinaService"),
            
            # 品种+日期参数集合
            "option_hist_shfe": ("app.services.data_sources.options.services.option_exchange_service", "OptionHistShfeService"),
            "option_hist_dce": ("app.services.data_sources.options.services.option_exchange_service", "OptionHistDceService"),
            "option_hist_czce": ("app.services.data_sources.options.services.option_exchange_service", "OptionHistCzceService"),
            "option_hist_gfex": ("app.services.data_sources.options.services.option_exchange_service", "OptionHistGfexService"),
        }
        
        self._service_classes = service_mappings
    
    def _get_service(self, collection_name: str):
        """获取或创建服务实例"""
        if collection_name in self._services:
            return self._services[collection_name]
        
        if collection_name not in self._service_classes:
            self.logger.warning(f"未找到集合 {collection_name} 的服务配置")
            return None
        
        module_path, class_name = self._service_classes[collection_name]
        
        try:
            import importlib
            module = importlib.import_module(module_path)
            service_class = getattr(module, class_name)
            service = service_class(self.db, self.task_manager)
            self._services[collection_name] = service
            return service
        except ImportError as e:
            self.logger.error(f"导入服务模块失败 {module_path}: {e}")
            return None
        except AttributeError as e:
            self.logger.error(f"服务类 {class_name} 不存在于模块 {module_path}: {e}")
            return None
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str = None,
        update_type: str = "batch",
        **kwargs
    ) -> Dict[str, Any]:
        """
        刷新指定集合的数据
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            update_type: 更新类型 "single" 或 "batch"
            **kwargs: 传递给服务的参数
            
        Returns:
            Dict包含刷新结果
        """
        # 验证集合配置
        config = get_collection_config(collection_name)
        if not config:
            return {
                "success": False,
                "message": f"未找到集合 {collection_name} 的配置"
            }
        
        # 获取服务实例
        service = self._get_service(collection_name)
        if not service:
            # 回退到使用旧的OptionDataService
            return await self._fallback_refresh(collection_name, task_id, **kwargs)
        
        try:
            # 更新任务状态
            if self.task_manager and task_id:
                await self.task_manager.update_task(
                    task_id,
                    status="running",
                    message=f"正在更新 {config['display_name']}..."
                )
            
            # 调用对应的更新方法
            if update_type == "single":
                result = await service.update_single_data(task_id=task_id, **kwargs)
            else:
                result = await service.update_batch_data(task_id=task_id, **kwargs)
            
            # 更新任务完成状态
            if self.task_manager and task_id:
                await self.task_manager.update_task(
                    task_id,
                    status="completed",
                    progress=100,
                    message=f"{config['display_name']} 更新完成"
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"刷新集合 {collection_name} 失败: {e}")
            
            if self.task_manager and task_id:
                await self.task_manager.update_task(
                    task_id,
                    status="failed",
                    message=f"更新失败: {str(e)}"
                )
            
            return {
                "success": False,
                "message": f"更新失败: {str(e)}"
            }
    
    async def _fallback_refresh(
        self,
        collection_name: str,
        task_id: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        回退到使用旧的OptionDataService
        用于尚未迁移到新架构的集合
        """
        try:
            from app.services.option_data_service import OptionDataService
            old_service = OptionDataService(self.db)
            
            # 调用旧服务的方法
            method_name = f"fetch_and_save_{collection_name}"
            if hasattr(old_service, method_name):
                method = getattr(old_service, method_name)
                result = await method(**kwargs)
                return {
                    "success": True,
                    "message": f"使用旧服务更新完成",
                    "data": result
                }
            else:
                return {
                    "success": False,
                    "message": f"旧服务中未找到方法 {method_name}"
                }
        except Exception as e:
            self.logger.error(f"回退刷新失败: {e}")
            return {
                "success": False,
                "message": f"回退刷新失败: {str(e)}"
            }
    
    async def clear_collection(self, collection_name: str) -> Dict[str, Any]:
        """清空指定集合的数据"""
        service = self._get_service(collection_name)
        
        if service:
            return await service.clear_data()
        
        # 回退到直接操作数据库
        try:
            collection = self.db[collection_name]
            result = await collection.delete_many({})
            return {
                "success": True,
                "deleted_count": result.deleted_count,
                "message": f"已删除 {result.deleted_count} 条数据"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"清空失败: {str(e)}"
            }
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """获取集合统计信息"""
        service = self._get_service(collection_name)
        
        if service:
            return await service.get_stats()
        
        # 回退到直接查询数据库
        try:
            collection = self.db[collection_name]
            count = await collection.count_documents({})
            return {
                "total_count": count,
                "collection_name": collection_name
            }
        except Exception as e:
            return {
                "total_count": 0,
                "error": str(e)
            }
    
    def get_supported_collections(self) -> List[str]:
        """获取支持的集合列表"""
        return list(OPTION_UPDATE_CONFIGS.keys())
    
    def get_collection_config(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """获取集合配置"""
        return get_collection_config(collection_name)
