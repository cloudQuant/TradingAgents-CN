"""货币报价时间序列数据测试"""
import unittest
from test_base import CurrenciesCollectionTestBase


class TestCurrencyTimeSeries(CurrenciesCollectionTestBase):
    """货币报价时间序列数据测试类"""
    collection_name = "currency_time_series"
    display_name = "货币报价时间序列数据"
    provider_class_name = "CurrencyTimeSeriesProvider"
    service_class_name = "CurrencyTimeSeriesService"
    is_simple_provider = False
    required_params = ["base", "start_date", "end_date", "api_key"]


if __name__ == "__main__":
    unittest.main()
