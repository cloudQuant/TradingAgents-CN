"""深交所当日合约数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCurrentDaySzseService(SimpleService):
    """深交所当日合约数据服务"""
    collection_name = "option_current_day_szse"
