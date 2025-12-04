"""期货手续费与保证金数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesCommInfoCollection(FuturesCollectionTestBase):
    """测试期货手续费与保证金数据集合"""
    collection_name = "futures_comm_info"
    display_name = "期货手续费与保证金"


if __name__ == "__main__":
    test = TestFuturesCommInfoCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
