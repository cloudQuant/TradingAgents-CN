"""成交持仓-新浪数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesHoldPosSinaCollection(FuturesCollectionTestBase):
    """测试成交持仓-新浪数据集合"""
    collection_name = "futures_hold_pos_sina"
    display_name = "成交持仓-新浪"


if __name__ == "__main__":
    test = TestFuturesHoldPosSinaCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
