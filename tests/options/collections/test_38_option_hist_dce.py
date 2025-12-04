"""大商所期权数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionHistDce(OptionsCollectionTestBase):
    """大商所期权数据测试类"""
    collection_name = "option_hist_dce"
    display_name = "大商所期权数据"
    provider_class_name = "OptionHistDceProvider"
    service_class_name = "OptionHistDceService"
    is_simple_provider = False
    required_params = ["symbol", "date"]


if __name__ == "__main__":
    unittest.main()
