"""
公司动态服务

东方财富网-数据中心-股市日历-公司动态
接口: stock_gsrl_gsdt_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gsrl_gsdt_em_provider import StockGsrlGsdtEmProvider


class StockGsrlGsdtEmService(BaseService):
    """公司动态服务"""
    
    collection_name = "stock_gsrl_gsdt_em"
    provider_class = StockGsrlGsdtEmProvider
    
    # 时间字段名
    time_field = "更新时间"
