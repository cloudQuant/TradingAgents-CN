"""货币报价时间序列数据服务"""
from app.services.data_sources.base_service import SimpleService


class CurrencyTimeSeriesService(SimpleService):
    """货币报价时间序列数据服务"""
    collection_name = "currency_time_series"
