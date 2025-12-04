"""期权日数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseDailySina(OptionsCollectionTestBase):
    """期权日数据测试类"""
    collection_name = "option_sse_daily_sina"
    display_name = "期权日数据"
    provider_class_name = "OptionSseDailySinaProvider"
    service_class_name = "OptionSseDailySinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
