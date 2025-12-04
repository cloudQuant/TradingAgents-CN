"""
个股商誉明细服务

东方财富网-数据中心-特色数据-商誉-个股商誉明细
接口: stock_sy_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sy_em_provider import StockSyEmProvider


class StockSyEmService(BaseService):
    """个股商誉明细服务"""
    
    collection_name = "stock_sy_em"
    provider_class = StockSyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
