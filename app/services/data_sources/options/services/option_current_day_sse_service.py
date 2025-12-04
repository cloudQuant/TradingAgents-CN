"""上交所当日合约数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCurrentDaySseService(SimpleService):
    """上交所当日合约数据服务"""
    collection_name = "option_current_day_sse"
