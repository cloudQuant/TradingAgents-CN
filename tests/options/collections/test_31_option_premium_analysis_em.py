"""期权折溢价测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionPremiumAnalysisEm(OptionsCollectionTestBase):
    """期权折溢价测试类"""
    collection_name = "option_premium_analysis_em"
    display_name = "期权折溢价"
    provider_class_name = "OptionPremiumAnalysisEmProvider"
    service_class_name = "OptionPremiumAnalysisEmService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
