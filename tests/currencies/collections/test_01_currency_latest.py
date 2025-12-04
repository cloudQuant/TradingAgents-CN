"""货币报价最新数据测试"""
import unittest
from test_base import CurrenciesCollectionTestBase


class TestCurrencyLatest(CurrenciesCollectionTestBase):
    """货币报价最新数据测试类"""
    collection_name = "currency_latest"
    display_name = "货币报价最新数据"
    provider_class_name = "CurrencyLatestProvider"
    service_class_name = "CurrencyLatestService"
    is_simple_provider = False
    required_params = ["base", "api_key"]


if __name__ == "__main__":
    unittest.main()
