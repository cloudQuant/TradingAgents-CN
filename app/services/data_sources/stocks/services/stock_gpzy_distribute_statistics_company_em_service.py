"""
质押机构分布统计-证券公司服务

东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司
接口: stock_gpzy_distribute_statistics_company_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_gpzy_distribute_statistics_company_em_provider import StockGpzyDistributeStatisticsCompanyEmProvider


class StockGpzyDistributeStatisticsCompanyEmService(SimpleService):
    """质押机构分布统计-证券公司服务"""
    
    collection_name = "stock_gpzy_distribute_statistics_company_em"
    provider_class = StockGpzyDistributeStatisticsCompanyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
