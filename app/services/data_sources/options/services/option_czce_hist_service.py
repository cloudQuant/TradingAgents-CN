"""郑商所期权历史行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCzceHistService(SimpleService):
    """郑商所期权历史行情数据服务"""
    collection_name = "option_czce_hist"
