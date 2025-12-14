"""深交所当日合约数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_current_day_szse_provider import OptionCurrentDaySzseProvider


class OptionCurrentDaySzseService(SimpleService):
    """深交所当日合约数据服务"""
    collection_name = "option_current_day_szse"
    provider_class = OptionCurrentDaySzseProvider
