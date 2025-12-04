"""
分时数据-东财服务

东方财富网-行情首页-港股-每日分时行情
接口: stock_hk_hist_min_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_hist_min_em_provider import StockHkHistMinEmProvider


class StockHkHistMinEmService(BaseService):
    """分时数据-东财服务"""
    
    collection_name = "stock_hk_hist_min_em"
    provider_class = StockHkHistMinEmProvider
    
    # 时间字段名
    time_field = "更新时间"
