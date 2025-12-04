"""
历史行情数据-东财服务

东方财富网-行情-美股-每日行情
接口: stock_us_hist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_us_hist_provider import StockUsHistProvider


class StockUsHistService(BaseService):
    """历史行情数据-东财服务"""
    
    collection_name = "stock_us_hist"
    provider_class = StockUsHistProvider
    
    # 时间字段名
    time_field = "更新时间"
