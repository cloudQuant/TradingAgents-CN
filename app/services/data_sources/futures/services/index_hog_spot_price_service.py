"""
生猪市场价格指数服务

无参数接口，只需要更新功能
"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.index_hog_spot_price_provider import IndexHogSpotPriceProvider


class IndexHogSpotPriceService(SimpleService):
    """生猪市场价格指数服务"""
    
    collection_name = "index_hog_spot_price"
    provider_class = IndexHogSpotPriceProvider
    
    time_field = "日期"
    unique_keys = ["日期"]
