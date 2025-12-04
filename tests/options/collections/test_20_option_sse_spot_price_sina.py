"""期权实时数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseSpotPriceSina(OptionsCollectionTestBase):
    """期权实时数据测试类"""
    collection_name = "option_sse_spot_price_sina"
    display_name = "期权实时数据"
    provider_class_name = "OptionSseSpotPriceSinaProvider"
    service_class_name = "OptionSseSpotPriceSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
