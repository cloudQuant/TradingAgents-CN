"""
新股发行服务

新浪财经-发行与分配-新股发行
接口: stock_ipo_info
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_ipo_info_provider import StockIpoInfoProvider


class StockIpoInfoService(BaseService):
    """新股发行服务"""
    
    collection_name = "stock_ipo_info"
    provider_class = StockIpoInfoProvider
    
    # 时间字段名
    time_field = "更新时间"
