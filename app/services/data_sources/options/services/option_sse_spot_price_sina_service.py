"""期权实时数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseSpotPriceSinaService(SimpleService):
    """期权实时数据服务"""
    collection_name = "option_sse_spot_price_sina"
