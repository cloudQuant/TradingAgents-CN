"""中金所沪深300指数实时行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCffexHs300SpotSina(OptionsCollectionTestBase):
    """中金所沪深300指数实时行情测试类"""
    collection_name = "option_cffex_hs300_spot_sina"
    display_name = "中金所沪深300指数实时行情"
    provider_class_name = "OptionCffexHs300SpotSinaProvider"
    service_class_name = "OptionCffexHs300SpotSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
