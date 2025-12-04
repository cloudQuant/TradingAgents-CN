"""货币对价格转换测试"""
import unittest
from test_base import CurrenciesCollectionTestBase


class TestCurrencyConvert(CurrenciesCollectionTestBase):
    """货币对价格转换测试类"""
    collection_name = "currency_convert"
    display_name = "货币对价格转换"
    provider_class_name = "CurrencyConvertProvider"
    service_class_name = "CurrencyConvertService"
    is_simple_provider = False
    required_params = ["base", "to", "amount", "api_key"]


if __name__ == "__main__":
    unittest.main()
