"""生猪-核心数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesHogCoreService(SimpleService):
    """生猪-核心数据服务"""
    collection_name = "futures_hog_core"
