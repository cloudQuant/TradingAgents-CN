"""期权标的物实时数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseUnderlyingSpotPriceSina(OptionsCollectionTestBase):
    """期权标的物实时数据测试类"""
    collection_name = "option_sse_underlying_spot_price_sina"
    display_name = "期权标的物实时数据"
    provider_class_name = "OptionSseUnderlyingSpotPriceSinaProvider"
    service_class_name = "OptionSseUnderlyingSpotPriceSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
