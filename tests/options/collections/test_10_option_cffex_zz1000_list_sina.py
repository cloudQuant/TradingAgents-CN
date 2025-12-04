"""中金所中证1000指数合约列表测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexZz1000ListSina(OptionsCollectionTestBase):
    """中金所中证1000指数合约列表测试类"""
    collection_name = "option_cffex_zz1000_list_sina"
    display_name = "中金所中证1000指数合约列表"
    provider_class_name = "OptionCffexZz1000ListSinaProvider"
    service_class_name = "OptionCffexZz1000ListSinaService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
