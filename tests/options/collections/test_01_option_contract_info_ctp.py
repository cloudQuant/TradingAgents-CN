"""openctp期权合约信息测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionContractInfoCtp(OptionsCollectionTestBase):
    """openctp期权合约信息测试类"""
    collection_name = "option_contract_info_ctp"
    display_name = "openctp期权合约信息"
    provider_class_name = "OptionContractInfoCtpProvider"
    service_class_name = "OptionContractInfoCtpService"
    is_simple_provider = True


if __name__ == "__main__":
    unittest.main()
