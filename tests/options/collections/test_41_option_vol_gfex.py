"""广期所隐含波动率测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionVolGfex(OptionsCollectionTestBase):
    """广期所隐含波动率测试类"""
    collection_name = "option_vol_gfex"
    display_name = "广期所隐含波动率"
    provider_class_name = "OptionVolGfexProvider"
    service_class_name = "OptionVolGfexService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
