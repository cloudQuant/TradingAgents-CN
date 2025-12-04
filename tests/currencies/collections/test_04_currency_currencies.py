"""货币基础信息查询测试"""
import unittest
from test_base import CurrenciesCollectionTestBase


class TestCurrencyCurrencies(CurrenciesCollectionTestBase):
    """货币基础信息查询测试类"""
    collection_name = "currency_currencies"
    display_name = "货币基础信息查询"
    provider_class_name = "CurrencyCurrenciesProvider"
    service_class_name = "CurrencyCurrenciesService"
    is_simple_provider = False
    required_params = ["c_type", "api_key"]


if __name__ == "__main__":
    unittest.main()
