"""金融期权行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_finance_board_provider import OptionFinanceBoardProvider


class OptionFinanceBoardService(SimpleService):
    """金融期权行情数据服务"""
    collection_name = "option_finance_board"
    provider_class = OptionFinanceBoardProvider
