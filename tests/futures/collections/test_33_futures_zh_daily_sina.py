"""内盘-历史行情数据-新浪数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesZhDailySinaCollection(FuturesCollectionTestBase):
    """测试内盘-历史行情数据-新浪数据集合"""
    collection_name = "futures_zh_daily_sina"
    display_name = "内盘-历史行情数据-新浪"


if __name__ == "__main__":
    test = TestFuturesZhDailySinaCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
