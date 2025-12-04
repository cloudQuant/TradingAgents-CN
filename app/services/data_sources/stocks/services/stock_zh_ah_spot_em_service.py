"""
实时行情数据-东财服务

东方财富网-行情中心-沪深港通-AH股比价-实时行情, 延迟 15 分钟更新
接口: stock_zh_ah_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_ah_spot_em_provider import StockZhAhSpotEmProvider


class StockZhAhSpotEmService(SimpleService):
    """实时行情数据-东财服务"""
    
    collection_name = "stock_zh_ah_spot_em"
    provider_class = StockZhAhSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
