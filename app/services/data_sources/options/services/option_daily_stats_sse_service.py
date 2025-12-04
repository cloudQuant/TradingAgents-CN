"""上交所每日统计数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionDailyStatsSseService(SimpleService):
    """上交所每日统计数据服务"""
    collection_name = "option_daily_stats_sse"
