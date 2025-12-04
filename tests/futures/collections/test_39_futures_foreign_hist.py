"""外盘-历史行情数据-新浪数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesForeignHistCollection(FuturesCollectionTestBase):
    """测试外盘-历史行情数据-新浪数据集合"""
    collection_name = "futures_foreign_hist"
    display_name = "外盘-历史行情数据-新浪"


if __name__ == "__main__":
    test = TestFuturesForeignHistCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
