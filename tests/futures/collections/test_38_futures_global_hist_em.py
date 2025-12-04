"""外盘-历史行情数据-东财数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesGlobalHistEmCollection(FuturesCollectionTestBase):
    """测试外盘-历史行情数据-东财数据集合"""
    collection_name = "futures_global_hist_em"
    display_name = "外盘-历史行情数据-东财"


if __name__ == "__main__":
    test = TestFuturesGlobalHistEmCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
