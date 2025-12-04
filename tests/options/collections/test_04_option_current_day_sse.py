"""上交所当日合约测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCurrentDaySse(OptionsCollectionTestBase):
    """上交所当日合约测试类"""
    collection_name = "option_current_day_sse"
    display_name = "上交所当日合约"
    provider_class_name = "OptionCurrentDaySseProvider"
    service_class_name = "OptionCurrentDaySseService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
