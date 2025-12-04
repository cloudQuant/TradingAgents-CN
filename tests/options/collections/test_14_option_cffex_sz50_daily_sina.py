"""中金所上证50指数日频行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexSz50DailySina(OptionsCollectionTestBase):
    """中金所上证50指数日频行情测试类"""
    collection_name = "option_cffex_sz50_daily_sina"
    display_name = "中金所上证50指数日频行情"
    provider_class_name = "OptionCffexSz50DailySinaProvider"
    service_class_name = "OptionCffexSz50DailySinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
