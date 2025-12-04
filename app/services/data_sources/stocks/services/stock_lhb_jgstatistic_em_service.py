"""
机构席位追踪服务

东方财富网-数据中心-龙虎榜单-机构席位追踪
接口: stock_lhb_jgstatistic_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_jgstatistic_em_provider import StockLhbJgstatisticEmProvider


class StockLhbJgstatisticEmService(BaseService):
    """机构席位追踪服务"""
    
    collection_name = "stock_lhb_jgstatistic_em"
    provider_class = StockLhbJgstatisticEmProvider
    
    # 时间字段名
    time_field = "更新时间"
