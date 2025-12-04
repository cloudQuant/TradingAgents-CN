"""广期所期权数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionHistGfex(OptionsCollectionTestBase):
    """广期所期权数据测试类"""
    collection_name = "option_hist_gfex"
    display_name = "广期所期权数据"
    provider_class_name = "OptionHistGfexProvider"
    service_class_name = "OptionHistGfexService"
    is_simple_provider = False
    required_params = ["symbol", "date"]


if __name__ == "__main__":
    unittest.main()
