"""内盘-历史行情数据-交易所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestGetFuturesDailyCollection(FuturesCollectionTestBase):
    """测试内盘-历史行情数据-交易所数据集合"""
    collection_name = "get_futures_daily"
    display_name = "内盘-历史行情数据-交易所"


if __name__ == "__main__":
    test = TestGetFuturesDailyCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
