"""上交所每日统计测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionDailyStatsSse(OptionsCollectionTestBase):
    """上交所每日统计测试类"""
    collection_name = "option_daily_stats_sse"
    display_name = "上交所每日统计"
    provider_class_name = "OptionDailyStatsSseProvider"
    service_class_name = "OptionDailyStatsSseService"
    is_simple_provider = False
    required_params = ["date"]


if __name__ == "__main__":
    unittest.main()
