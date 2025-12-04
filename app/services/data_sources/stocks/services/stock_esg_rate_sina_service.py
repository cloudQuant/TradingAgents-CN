"""
ESG 评级数据服务

新浪财经-ESG评级中心-ESG评级-ESG评级数据
接口: stock_esg_rate_sina
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_esg_rate_sina_provider import StockEsgRateSinaProvider


class StockEsgRateSinaService(SimpleService):
    """ESG 评级数据服务"""
    
    collection_name = "stock_esg_rate_sina"
    provider_class = StockEsgRateSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
