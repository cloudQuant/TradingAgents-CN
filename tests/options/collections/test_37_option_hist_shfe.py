"""上期所期权数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionHistShfe(OptionsCollectionTestBase):
    """上期所期权数据测试类"""
    collection_name = "option_hist_shfe"
    display_name = "上期所期权数据"
    provider_class_name = "OptionHistShfeProvider"
    service_class_name = "OptionHistShfeService"
    is_simple_provider = False
    required_params = ["symbol", "date"]


if __name__ == "__main__":
    unittest.main()
