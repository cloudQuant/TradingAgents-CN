"""期权日数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseDailySinaService(SimpleService):
    """期权日数据服务"""
    collection_name = "option_sse_daily_sina"
