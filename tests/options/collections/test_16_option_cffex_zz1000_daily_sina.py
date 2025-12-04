"""中金所中证1000指数日频行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexZz1000DailySina(OptionsCollectionTestBase):
    """中金所中证1000指数日频行情测试类"""
    collection_name = "option_cffex_zz1000_daily_sina"
    display_name = "中金所中证1000指数日频行情"
    provider_class_name = "OptionCffexZz1000DailySinaProvider"
    service_class_name = "OptionCffexZz1000DailySinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
