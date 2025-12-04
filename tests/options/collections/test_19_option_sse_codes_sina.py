"""看涨看跌合约代码测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseCodesSina(OptionsCollectionTestBase):
    """看涨看跌合约代码测试类"""
    collection_name = "option_sse_codes_sina"
    display_name = "看涨看跌合约代码"
    provider_class_name = "OptionSseCodesSinaProvider"
    service_class_name = "OptionSseCodesSinaService"
    is_simple_provider = False
    required_params = ["trade_date", "underlying"]


if __name__ == "__main__":
    unittest.main()
