"""内盘-分时行情数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesZhMinuteSinaCollection(FuturesCollectionTestBase):
    """测试内盘-分时行情数据集合"""
    collection_name = "futures_zh_minute_sina"
    display_name = "内盘-分时行情数据"


if __name__ == "__main__":
    test = TestFuturesZhMinuteSinaCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
