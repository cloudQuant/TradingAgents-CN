"""东财期权行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCurrentEm(OptionsCollectionTestBase):
    """东财期权行情测试类"""
    collection_name = "option_current_em"
    display_name = "东财期权行情"
    provider_class_name = "OptionCurrentEmProvider"
    service_class_name = "OptionCurrentEmService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
