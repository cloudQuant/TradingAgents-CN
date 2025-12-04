"""
机构调研-详细服务

东方财富网-数据中心-特色数据-机构调研-机构调研详细
接口: stock_jgdy_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_jgdy_detail_em_provider import StockJgdyDetailEmProvider


class StockJgdyDetailEmService(BaseService):
    """机构调研-详细服务"""
    
    collection_name = "stock_jgdy_detail_em"
    provider_class = StockJgdyDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
