"""
路孚特服务

新浪财经-ESG评级中心-ESG评级-路孚特
接口: stock_esg_rft_sina
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_esg_rft_sina_provider import StockEsgRftSinaProvider


class StockEsgRftSinaService(SimpleService):
    """路孚特服务"""
    
    collection_name = "stock_esg_rft_sina"
    provider_class = StockEsgRftSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
