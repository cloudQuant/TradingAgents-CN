"""大连商品交易所-合约信息数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractInfoDceCollection(FuturesCollectionTestBase):
    """测试大连商品交易所-合约信息数据集合"""
    collection_name = "futures_contract_info_dce"
    display_name = "大连商品交易所-合约信息"


if __name__ == "__main__":
    test = TestFuturesContractInfoDceCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
