"""
分时数据-东财服务

东方财富网-行情首页-美股-每日分时行情
接口: stock_us_hist_min_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_us_hist_min_em_provider import StockUsHistMinEmProvider


class StockUsHistMinEmService(BaseService):
    """分时数据-东财服务"""
    
    collection_name = "stock_us_hist_min_em"
    provider_class = StockUsHistMinEmProvider
    
    # 时间字段名
    time_field = "更新时间"
