"""内盘-实时行情数据(品种)数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesZhRealtimeCollection(FuturesCollectionTestBase):
    """测试内盘-实时行情数据(品种)数据集合"""
    collection_name = "futures_zh_realtime"
    display_name = "内盘-实时行情数据(品种)"


if __name__ == "__main__":
    test = TestFuturesZhRealtimeCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
