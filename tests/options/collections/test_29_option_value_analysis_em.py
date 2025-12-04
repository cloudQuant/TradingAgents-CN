"""期权价值分析测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionValueAnalysisEm(OptionsCollectionTestBase):
    """期权价值分析测试类"""
    collection_name = "option_value_analysis_em"
    display_name = "期权价值分析"
    provider_class_name = "OptionValueAnalysisEmProvider"
    service_class_name = "OptionValueAnalysisEmService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
