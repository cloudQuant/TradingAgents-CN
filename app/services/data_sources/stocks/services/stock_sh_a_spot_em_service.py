"""
沪 A 股服务

东方财富网-沪 A 股-实时行情数据
接口: stock_sh_a_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_sh_a_spot_em_provider import StockShASpotEmProvider


class StockShASpotEmService(SimpleService):
    """沪 A 股服务"""
    
    collection_name = "stock_sh_a_spot_em"
    provider_class = StockShASpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
