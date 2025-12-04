"""期货合约详情-东财数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractDetailEmCollection(FuturesCollectionTestBase):
    """测试期货合约详情-东财数据集合"""
    collection_name = "futures_contract_detail_em"
    display_name = "期货合约详情-东财"


if __name__ == "__main__":
    test = TestFuturesContractDetailEmCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
