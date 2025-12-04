"""生猪-供应维度服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesHogSupplyService(SimpleService):
    """生猪-供应维度服务"""
    collection_name = "futures_hog_supply"
