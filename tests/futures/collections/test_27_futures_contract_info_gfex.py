"""广州期货交易所-合约信息数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractInfoGfexCollection(FuturesCollectionTestBase):
    """测试广州期货交易所-合约信息数据集合"""
    collection_name = "futures_contract_info_gfex"
    display_name = "广州期货交易所-合约信息"


if __name__ == "__main__":
    test = TestFuturesContractInfoGfexCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
