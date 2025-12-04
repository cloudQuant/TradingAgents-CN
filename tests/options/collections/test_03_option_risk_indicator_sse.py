"""上交所期权风险指标测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionRiskIndicatorSse(OptionsCollectionTestBase):
    """上交所期权风险指标测试类"""
    collection_name = "option_risk_indicator_sse"
    display_name = "上交所期权风险指标"
    provider_class_name = "OptionRiskIndicatorSseProvider"
    service_class_name = "OptionRiskIndicatorSseService"
    is_simple_provider = False
    required_params = ["date"]


if __name__ == "__main__":
    unittest.main()
