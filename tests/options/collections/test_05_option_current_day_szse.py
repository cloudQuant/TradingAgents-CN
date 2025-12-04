"""深交所当日合约测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCurrentDaySzse(OptionsCollectionTestBase):
    """深交所当日合约测试类"""
    collection_name = "option_current_day_szse"
    display_name = "深交所当日合约"
    provider_class_name = "OptionCurrentDaySzseProvider"
    service_class_name = "OptionCurrentDaySzseService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
