"""中国金融期货交易所-合约信息数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractInfoCffexCollection(FuturesCollectionTestBase):
    """测试中国金融期货交易所-合约信息数据集合"""
    collection_name = "futures_contract_info_cffex"
    display_name = "中国金融期货交易所-合约信息"


if __name__ == "__main__":
    test = TestFuturesContractInfoCffexCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
