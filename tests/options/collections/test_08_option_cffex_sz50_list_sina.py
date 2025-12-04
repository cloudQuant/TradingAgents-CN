"""中金所上证50指数合约列表测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexSz50ListSina(OptionsCollectionTestBase):
    """中金所上证50指数合约列表测试类"""
    collection_name = "option_cffex_sz50_list_sina"
    display_name = "中金所上证50指数合约列表"
    provider_class_name = "OptionCffexSz50ListSinaProvider"
    service_class_name = "OptionCffexSz50ListSinaService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
