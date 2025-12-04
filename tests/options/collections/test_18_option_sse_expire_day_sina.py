"""剩余到期时间测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionSseExpireDaySina(OptionsCollectionTestBase):
    """剩余到期时间测试类"""
    collection_name = "option_sse_expire_day_sina"
    display_name = "剩余到期时间"
    provider_class_name = "OptionSseExpireDaySinaProvider"
    service_class_name = "OptionSseExpireDaySinaService"
    is_simple_provider = False
    required_params = ["trade_date", "symbol"]


if __name__ == "__main__":
    unittest.main()
