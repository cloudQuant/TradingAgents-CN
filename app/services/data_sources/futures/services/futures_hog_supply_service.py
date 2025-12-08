"""生猪-供应维度服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_hog_supply_provider import FuturesHogSupplyProvider


class FuturesHogSupplyService(SimpleService):
    """生猪-供应维度服务"""
    collection_name = "futures_hog_supply"
    provider_class = FuturesHogSupplyProvider
