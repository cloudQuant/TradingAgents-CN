"""
北交所服务

东方财富网-数据中心-新股数据-IPO审核信息-北交所
接口: stock_register_bj
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_register_bj_provider import StockRegisterBjProvider


class StockRegisterBjService(SimpleService):
    """北交所服务"""
    
    collection_name = "stock_register_bj"
    provider_class = StockRegisterBjProvider
    
    # 时间字段名
    time_field = "更新时间"
