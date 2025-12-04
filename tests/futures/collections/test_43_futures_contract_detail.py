"""期货合约详情-新浪数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractDetailCollection(FuturesCollectionTestBase):
    """测试期货合约详情-新浪数据集合"""
    collection_name = "futures_contract_detail"
    display_name = "期货合约详情-新浪"


if __name__ == "__main__":
    test = TestFuturesContractDetailCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
