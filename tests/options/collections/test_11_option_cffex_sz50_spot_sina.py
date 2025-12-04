"""中金所上证50指数实时行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexSz50SpotSina(OptionsCollectionTestBase):
    """中金所上证50指数实时行情测试类"""
    collection_name = "option_cffex_sz50_spot_sina"
    display_name = "中金所上证50指数实时行情"
    provider_class_name = "OptionCffexSz50SpotSinaProvider"
    service_class_name = "OptionCffexSz50SpotSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
