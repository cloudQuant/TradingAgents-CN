"""
机构调研-统计服务

东方财富网-数据中心-特色数据-机构调研-机构调研统计
接口: stock_jgdy_tj_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_jgdy_tj_em_provider import StockJgdyTjEmProvider


class StockJgdyTjEmService(BaseService):
    """机构调研-统计服务"""
    
    collection_name = "stock_jgdy_tj_em"
    provider_class = StockJgdyTjEmProvider
    
    # 时间字段名
    time_field = "更新时间"
