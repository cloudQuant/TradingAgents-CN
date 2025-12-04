"""
上海主板服务

东方财富网-数据中心-新股数据-IPO审核信息-上海主板
接口: stock_register_sh
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_register_sh_provider import StockRegisterShProvider


class StockRegisterShService(SimpleService):
    """上海主板服务"""
    
    collection_name = "stock_register_sh"
    provider_class = StockRegisterShProvider
    
    # 时间字段名
    time_field = "更新时间"
