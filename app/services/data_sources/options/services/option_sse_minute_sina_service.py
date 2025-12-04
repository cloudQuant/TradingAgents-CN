"""期权分钟数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseMinuteSinaService(SimpleService):
    """期权分钟数据服务"""
    collection_name = "option_sse_minute_sina"
