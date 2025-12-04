"""
知名港股服务

东方财富网-行情中心-港股市场-知名港股实时行情数据
接口: stock_hk_famous_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hk_famous_spot_em_provider import StockHkFamousSpotEmProvider


class StockHkFamousSpotEmService(SimpleService):
    """知名港股服务"""
    
    collection_name = "stock_hk_famous_spot_em"
    provider_class = StockHkFamousSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
