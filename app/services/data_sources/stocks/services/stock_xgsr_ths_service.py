"""
新股上市首日服务

同花顺-数据中心-新股数据-新股上市首日
接口: stock_xgsr_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_xgsr_ths_provider import StockXgsrThsProvider


class StockXgsrThsService(SimpleService):
    """新股上市首日服务"""
    
    collection_name = "stock_xgsr_ths"
    provider_class = StockXgsrThsProvider
    
    # 时间字段名
    time_field = "更新时间"
