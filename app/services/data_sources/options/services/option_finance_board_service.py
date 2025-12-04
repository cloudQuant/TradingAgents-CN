"""金融期权行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionFinanceBoardService(SimpleService):
    """金融期权行情数据服务"""
    collection_name = "option_finance_board"
