"""
A股商誉市场概况服务

东方财富网-数据中心-特色数据-商誉-A股商誉市场概况
接口: stock_sy_profile_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_sy_profile_em_provider import StockSyProfileEmProvider


class StockSyProfileEmService(SimpleService):
    """A股商誉市场概况服务"""
    
    collection_name = "stock_sy_profile_em"
    provider_class = StockSyProfileEmProvider
    
    # 时间字段名
    time_field = "更新时间"
