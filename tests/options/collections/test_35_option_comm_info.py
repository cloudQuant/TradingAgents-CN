"""商品期权手续费测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCommInfo(OptionsCollectionTestBase):
    """商品期权手续费测试类"""
    collection_name = "option_comm_info"
    display_name = "商品期权手续费"
    provider_class_name = "OptionCommInfoProvider"
    service_class_name = "OptionCommInfoService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
