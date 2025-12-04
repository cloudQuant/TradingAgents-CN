"""金融期权股票期权分时行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionFinanceMinuteSina(OptionsCollectionTestBase):
    """金融期权股票期权分时行情测试类"""
    collection_name = "option_finance_minute_sina"
    display_name = "金融期权股票期权分时行情"
    provider_class_name = "OptionFinanceMinuteSinaProvider"
    service_class_name = "OptionFinanceMinuteSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
