"""内盘-实时行情数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesZhSpotCollection(FuturesCollectionTestBase):
    """测试内盘-实时行情数据集合"""
    collection_name = "futures_zh_spot"
    display_name = "内盘-实时行情数据"


if __name__ == "__main__":
    test = TestFuturesZhSpotCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
