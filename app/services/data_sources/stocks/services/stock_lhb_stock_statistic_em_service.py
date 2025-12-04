"""
个股上榜统计服务

东方财富网-数据中心-龙虎榜单-个股上榜统计
接口: stock_lhb_stock_statistic_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_stock_statistic_em_provider import StockLhbStockStatisticEmProvider


class StockLhbStockStatisticEmService(BaseService):
    """个股上榜统计服务"""
    
    collection_name = "stock_lhb_stock_statistic_em"
    provider_class = StockLhbStockStatisticEmProvider
    
    # 时间字段名
    time_field = "更新时间"
