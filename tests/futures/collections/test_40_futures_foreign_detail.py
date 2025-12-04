"""外盘-合约详情数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesForeignDetailCollection(FuturesCollectionTestBase):
    """测试外盘-合约详情数据集合"""
    collection_name = "futures_foreign_detail"
    display_name = "外盘-合约详情"


if __name__ == "__main__":
    test = TestFuturesForeignDetailCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
