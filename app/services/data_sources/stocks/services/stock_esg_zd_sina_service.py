"""
秩鼎服务

新浪财经-ESG评级中心-ESG评级-秩鼎
接口: stock_esg_zd_sina
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_esg_zd_sina_provider import StockEsgZdSinaProvider


class StockEsgZdSinaService(SimpleService):
    """秩鼎服务"""
    
    collection_name = "stock_esg_zd_sina"
    provider_class = StockEsgZdSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
