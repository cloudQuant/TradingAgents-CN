"""
个股商誉减值明细服务

东方财富网-数据中心-特色数据-商誉-个股商誉减值明细
接口: stock_sy_jz_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sy_jz_em_provider import StockSyJzEmProvider


class StockSyJzEmService(BaseService):
    """个股商誉减值明细服务"""
    
    collection_name = "stock_sy_jz_em"
    provider_class = StockSyJzEmProvider
    
    # 时间字段名
    time_field = "更新时间"
