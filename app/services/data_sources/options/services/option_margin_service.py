"""期权保证金数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionMarginService(SimpleService):
    """期权保证金数据服务"""
    collection_name = "option_margin"
