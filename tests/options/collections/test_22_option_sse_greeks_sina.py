"""期权希腊字母信息表测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseGreeksSina(OptionsCollectionTestBase):
    """期权希腊字母信息表测试类"""
    collection_name = "option_sse_greeks_sina"
    display_name = "期权希腊字母信息表"
    provider_class_name = "OptionSseGreeksSinaProvider"
    service_class_name = "OptionSseGreeksSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
