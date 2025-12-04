"""金融期权行情数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionFinanceBoard(OptionsCollectionTestBase):
    """金融期权行情数据测试类"""
    collection_name = "option_finance_board"
    display_name = "金融期权行情数据"
    provider_class_name = "OptionFinanceBoardProvider"
    service_class_name = "OptionFinanceBoardService"
    is_simple_provider = False
    required_params = ["symbol", "end_month"]


if __name__ == "__main__":
    unittest.main()
