"""
沪深京 A 股服务

东方财富网-沪深京 A 股-实时行情数据
接口: stock_zh_a_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_a_spot_em_provider import StockZhASpotEmProvider


class StockZhASpotEmService(SimpleService):
    """沪深京 A 股服务"""
    
    collection_name = "stock_zh_a_spot_em"
    provider_class = StockZhASpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
