"""期权分钟数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseMinuteSina(OptionsCollectionTestBase):
    """期权分钟数据测试类"""
    collection_name = "option_sse_minute_sina"
    display_name = "期权分钟数据"
    provider_class_name = "OptionSseMinuteSinaProvider"
    service_class_name = "OptionSseMinuteSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
