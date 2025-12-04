"""
实时行情数据-东财服务

东方财富网-实时行情数据
接口: stock_zh_b_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_b_spot_em_provider import StockZhBSpotEmProvider


class StockZhBSpotEmService(SimpleService):
    """实时行情数据-东财服务"""
    
    collection_name = "stock_zh_b_spot_em"
    provider_class = StockZhBSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
