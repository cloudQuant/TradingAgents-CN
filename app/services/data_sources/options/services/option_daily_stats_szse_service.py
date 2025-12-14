"""深交所日度概况数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_daily_stats_szse_provider import OptionDailyStatsSzseProvider


class OptionDailyStatsSzseService(SimpleService):
    """深交所日度概况数据服务"""
    collection_name = "option_daily_stats_szse"
    provider_class = OptionDailyStatsSzseProvider
