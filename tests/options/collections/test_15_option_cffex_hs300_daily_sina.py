"""中金所沪深300指数日频行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexHs300DailySina(OptionsCollectionTestBase):
    """中金所沪深300指数日频行情测试类"""
    collection_name = "option_cffex_hs300_daily_sina"
    display_name = "中金所沪深300指数日频行情"
    provider_class_name = "OptionCffexHs300DailySinaProvider"
    service_class_name = "OptionCffexHs300DailySinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
