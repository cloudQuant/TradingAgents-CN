"""深交所日度概况数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionDailyStatsSzseService(SimpleService):
    """深交所日度概况数据服务"""
    collection_name = "option_daily_stats_szse"
