"""
破净股统计服务

乐咕乐股-A 股破净股统计数据
接口: stock_a_below_net_asset_statistics
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_a_below_net_asset_statistics_provider import StockABelowNetAssetStatisticsProvider


class StockABelowNetAssetStatisticsService(BaseService):
    """破净股统计服务"""
    
    collection_name = "stock_a_below_net_asset_statistics"
    provider_class = StockABelowNetAssetStatisticsProvider
    
    # 时间字段名
    time_field = "更新时间"
