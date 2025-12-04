"""上交所50ETF合约到期月份列表测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseListSina(OptionsCollectionTestBase):
    """上交所50ETF合约到期月份列表测试类"""
    collection_name = "option_sse_list_sina"
    display_name = "上交所50ETF合约到期月份列表"
    provider_class_name = "OptionSseListSinaProvider"
    service_class_name = "OptionSseListSinaService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
