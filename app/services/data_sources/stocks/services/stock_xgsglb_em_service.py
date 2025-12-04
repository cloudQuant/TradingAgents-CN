"""
新股申购与中签服务

东方财富网-数据中心-新股数据-新股申购-新股申购与中签查询
接口: stock_xgsglb_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_xgsglb_em_provider import StockXgsglbEmProvider


class StockXgsglbEmService(BaseService):
    """新股申购与中签服务"""
    
    collection_name = "stock_xgsglb_em"
    provider_class = StockXgsglbEmProvider
    
    # 时间字段名
    time_field = "更新时间"
