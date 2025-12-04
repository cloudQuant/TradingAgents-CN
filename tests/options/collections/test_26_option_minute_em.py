"""东财期权分时行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionMinuteEm(OptionsCollectionTestBase):
    """东财期权分时行情测试类"""
    collection_name = "option_minute_em"
    display_name = "东财期权分时行情"
    provider_class_name = "OptionMinuteEmProvider"
    service_class_name = "OptionMinuteEmService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
