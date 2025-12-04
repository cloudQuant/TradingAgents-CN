"""
分时数据-东财服务

东方财富网-行情首页-沪深京 A 股-每日分时行情; 该接口只能获取近期的分时数据，注意时间周期的设置
接口: stock_zh_a_hist_min_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_hist_min_em_provider import StockZhAHistMinEmProvider


class StockZhAHistMinEmService(BaseService):
    """分时数据-东财服务"""
    
    collection_name = "stock_zh_a_hist_min_em"
    provider_class = StockZhAHistMinEmProvider
    
    # 时间字段名
    time_field = "更新时间"
