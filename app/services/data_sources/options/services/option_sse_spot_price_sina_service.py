"""期权实时数据服务"""
from app.services.data_sources.base_service import BaseService
from app.services.data_sources.options.providers.option_sse_spot_price_sina_provider import OptionSseSpotPriceSinaProvider


class OptionSseSpotPriceSinaService(BaseService):
    """期权实时数据服务
    
    该接口需要symbol参数，用于获取指定合约的实时数据。
    """
    collection_name = "option_sse_spot_price_sina"
    provider_class = OptionSseSpotPriceSinaProvider
