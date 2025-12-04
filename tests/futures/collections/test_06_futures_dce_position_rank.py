"""大连商品交易所-持仓排名数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesDcePositionRankCollection(FuturesCollectionTestBase):
    """测试大连商品交易所-持仓排名数据集合"""
    collection_name = "futures_dce_position_rank"
    display_name = "大连商品交易所-持仓排名"


if __name__ == "__main__":
    test = TestFuturesDcePositionRankCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
