"""
知名美股服务

美股-知名美股的实时行情数据
接口: stock_us_famous_spot_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_us_famous_spot_em_provider import StockUsFamousSpotEmProvider


class StockUsFamousSpotEmService(BaseService):
    """知名美股服务"""
    
    collection_name = "stock_us_famous_spot_em"
    provider_class = StockUsFamousSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
