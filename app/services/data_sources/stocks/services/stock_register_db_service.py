"""
达标企业服务

东方财富网-数据中心-新股数据-注册制审核-达标企业
接口: stock_register_db
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_register_db_provider import StockRegisterDbProvider


class StockRegisterDbService(SimpleService):
    """达标企业服务"""
    
    collection_name = "stock_register_db"
    provider_class = StockRegisterDbProvider
    
    # 时间字段名
    time_field = "更新时间"
