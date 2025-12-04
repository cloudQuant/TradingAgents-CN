"""郑州商品交易所-合约信息数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractInfoCzceCollection(FuturesCollectionTestBase):
    """测试郑州商品交易所-合约信息数据集合"""
    collection_name = "futures_contract_info_czce"
    display_name = "郑州商品交易所-合约信息"


if __name__ == "__main__":
    test = TestFuturesContractInfoCzceCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
