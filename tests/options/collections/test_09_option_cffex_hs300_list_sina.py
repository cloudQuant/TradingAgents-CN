"""中金所沪深300指数合约列表测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexHs300ListSina(OptionsCollectionTestBase):
    """中金所沪深300指数合约列表测试类"""
    collection_name = "option_cffex_hs300_list_sina"
    display_name = "中金所沪深300指数合约列表"
    provider_class_name = "OptionCffexHs300ListSinaProvider"
    service_class_name = "OptionCffexHs300ListSinaService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
