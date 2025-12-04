"""期权风险分析测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionRiskAnalysisEm(OptionsCollectionTestBase):
    """期权风险分析测试类"""
    collection_name = "option_risk_analysis_em"
    display_name = "期权风险分析"
    provider_class_name = "OptionRiskAnalysisEmProvider"
    service_class_name = "OptionRiskAnalysisEmService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
