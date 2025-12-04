"""
MSCI服务

新浪财经-ESG评级中心-ESG评级-MSCI
接口: stock_esg_msci_sina
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_esg_msci_sina_provider import StockEsgMsciSinaProvider


class StockEsgMsciSinaService(SimpleService):
    """MSCI服务"""
    
    collection_name = "stock_esg_msci_sina"
    provider_class = StockEsgMsciSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
