"""期权保证金测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionMargin(OptionsCollectionTestBase):
    """期权保证金测试类"""
    collection_name = "option_margin"
    display_name = "期权保证金"
    provider_class_name = "OptionMarginProvider"
    service_class_name = "OptionMarginService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
