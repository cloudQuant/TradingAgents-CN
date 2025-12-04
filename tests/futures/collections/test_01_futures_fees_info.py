"""期货交易费用参照表数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesFeesInfoCollection(FuturesCollectionTestBase):
    """测试期货交易费用参照表数据集合"""
    collection_name = "futures_fees_info"
    display_name = "期货交易费用参照表"


if __name__ == "__main__":
    test = TestFuturesFeesInfoCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
