"""深交所日度概况测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionDailyStatsSzse(OptionsCollectionTestBase):
    """深交所日度概况测试类"""
    collection_name = "option_daily_stats_szse"
    display_name = "深交所日度概况"
    provider_class_name = "OptionDailyStatsSzseProvider"
    service_class_name = "OptionDailyStatsSzseService"
    is_simple_provider = False
    required_params = ["date"]


if __name__ == "__main__":
    unittest.main()
