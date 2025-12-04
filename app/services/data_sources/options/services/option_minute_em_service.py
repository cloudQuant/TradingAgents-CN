"""东财期权分时行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionMinuteEmService(SimpleService):
    """东财期权分时行情数据服务"""
    collection_name = "option_minute_em"
