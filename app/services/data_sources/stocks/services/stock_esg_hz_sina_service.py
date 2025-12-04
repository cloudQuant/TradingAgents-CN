"""
华证指数服务

新浪财经-ESG评级中心-ESG评级-华证指数
接口: stock_esg_hz_sina
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_esg_hz_sina_provider import StockEsgHzSinaProvider


class StockEsgHzSinaService(SimpleService):
    """华证指数服务"""
    
    collection_name = "stock_esg_hz_sina"
    provider_class = StockEsgHzSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
