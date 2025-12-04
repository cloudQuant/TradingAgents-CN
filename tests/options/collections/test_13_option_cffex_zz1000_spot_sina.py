"""中金所中证1000指数实时行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexZz1000SpotSina(OptionsCollectionTestBase):
    """中金所中证1000指数实时行情测试类"""
    collection_name = "option_cffex_zz1000_spot_sina"
    display_name = "中金所中证1000指数实时行情"
    provider_class_name = "OptionCffexZz1000SpotSinaProvider"
    service_class_name = "OptionCffexZz1000SpotSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
