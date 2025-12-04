"""
质押机构分布统计-银行服务

东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
接口: stock_gpzy_distribute_statistics_bank_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_gpzy_distribute_statistics_bank_em_provider import StockGpzyDistributeStatisticsBankEmProvider


class StockGpzyDistributeStatisticsBankEmService(SimpleService):
    """质押机构分布统计-银行服务"""
    
    collection_name = "stock_gpzy_distribute_statistics_bank_em"
    provider_class = StockGpzyDistributeStatisticsBankEmProvider
    
    # 时间字段名
    time_field = "更新时间"
