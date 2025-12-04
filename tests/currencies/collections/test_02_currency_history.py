"""货币报价历史数据测试"""
import unittest
from test_base import CurrenciesCollectionTestBase


class TestCurrencyHistory(CurrenciesCollectionTestBase):
    """货币报价历史数据测试类"""
    collection_name = "currency_history"
    display_name = "货币报价历史数据"
    provider_class_name = "CurrencyHistoryProvider"
    service_class_name = "CurrencyHistoryService"
    is_simple_provider = False
    required_params = ["base", "date", "api_key"]


if __name__ == "__main__":
    unittest.main()
