"""内盘-历史行情数据-东财数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesHistEmCollection(FuturesCollectionTestBase):
    """测试内盘-历史行情数据-东财数据集合"""
    collection_name = "futures_hist_em"
    display_name = "内盘-历史行情数据-东财"


if __name__ == "__main__":
    test = TestFuturesHistEmCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
