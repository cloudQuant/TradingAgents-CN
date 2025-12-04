"""
次新股服务

新浪财经-行情中心-沪深股市-次新股
接口: stock_zh_a_new
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_a_new_provider import StockZhANewProvider


class StockZhANewService(SimpleService):
    """次新股服务"""
    
    collection_name = "stock_zh_a_new"
    provider_class = StockZhANewProvider
    
    # 时间字段名
    time_field = "更新时间"
