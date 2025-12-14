"""上交所每日统计数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_daily_stats_sse_provider import OptionDailyStatsSseProvider


class OptionDailyStatsSseService(SimpleService):
    """上交所每日统计数据服务"""
    collection_name = "option_daily_stats_sse"
    provider_class = OptionDailyStatsSseProvider
