"""
实时行情数据服务

新浪财经-科创板股票实时行情数据
接口: stock_zh_kcb_spot
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_kcb_spot_provider import StockZhKcbSpotProvider


class StockZhKcbSpotService(SimpleService):
    """实时行情数据服务"""
    
    collection_name = "stock_zh_kcb_spot"
    provider_class = StockZhKcbSpotProvider
    
    # 时间字段名
    time_field = "更新时间"
