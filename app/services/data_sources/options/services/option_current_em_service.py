"""东财期权行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCurrentEmService(SimpleService):
    """东财期权行情数据服务"""
    collection_name = "option_current_em"
