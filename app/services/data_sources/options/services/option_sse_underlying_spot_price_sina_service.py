"""期权标的物实时数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_sse_underlying_spot_price_sina_provider import OptionSseUnderlyingSpotPriceSinaProvider


class OptionSseUnderlyingSpotPriceSinaService(SimpleService):
    """期权标的物实时数据服务"""
    collection_name = "option_sse_underlying_spot_price_sina"
    provider_class = OptionSseUnderlyingSpotPriceSinaProvider
