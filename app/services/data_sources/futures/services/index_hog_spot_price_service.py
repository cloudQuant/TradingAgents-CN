"""生猪市场价格指数服务"""
from app.services.data_sources.base_service import SimpleService


class IndexHogSpotPriceService(SimpleService):
    """生猪市场价格指数服务"""
    collection_name = "index_hog_spot_price"
