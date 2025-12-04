"""期货连续合约-新浪数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesMainSinaCollection(FuturesCollectionTestBase):
    """测试期货连续合约-新浪数据集合"""
    collection_name = "futures_main_sina"
    display_name = "期货连续合约-新浪"


if __name__ == "__main__":
    test = TestFuturesMainSinaCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
