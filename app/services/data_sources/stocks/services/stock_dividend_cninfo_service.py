"""
历史分红服务

巨潮资讯-个股-历史分红
接口: stock_dividend_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_dividend_cninfo_provider import StockDividendCninfoProvider


class StockDividendCninfoService(BaseService):
    """历史分红服务"""
    
    collection_name = "stock_dividend_cninfo"
    provider_class = StockDividendCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
