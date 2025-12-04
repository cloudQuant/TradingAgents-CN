"""期权龙虎榜测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionLhbEm(OptionsCollectionTestBase):
    """期权龙虎榜测试类"""
    collection_name = "option_lhb_em"
    display_name = "期权龙虎榜"
    provider_class_name = "OptionLhbEmProvider"
    service_class_name = "OptionLhbEmService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
