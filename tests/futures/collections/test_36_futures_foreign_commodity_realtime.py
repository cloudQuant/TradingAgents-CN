"""外盘-实时行情数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesForeignCommodityRealtimeCollection(FuturesCollectionTestBase):
    """测试外盘-实时行情数据集合"""
    collection_name = "futures_foreign_commodity_realtime"
    display_name = "外盘-实时行情数据"


if __name__ == "__main__":
    test = TestFuturesForeignCommodityRealtimeCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
