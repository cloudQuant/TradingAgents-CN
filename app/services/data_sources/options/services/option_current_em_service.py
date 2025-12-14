"""东财期权行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_current_em_provider import OptionCurrentEmProvider


class OptionCurrentEmService(SimpleService):
    """东财期权行情数据服务"""
    collection_name = "option_current_em"
    provider_class = OptionCurrentEmProvider
