"""
股票账户统计月度服务

东方财富网-数据中心-特色数据-股票账户统计
接口: stock_account_statistics_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_account_statistics_em_provider import StockAccountStatisticsEmProvider


class StockAccountStatisticsEmService(SimpleService):
    """股票账户统计月度服务"""
    
    collection_name = "stock_account_statistics_em"
    provider_class = StockAccountStatisticsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
