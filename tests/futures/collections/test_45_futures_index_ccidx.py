"""中证商品指数数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesIndexCcidxCollection(FuturesCollectionTestBase):
    """测试中证商品指数数据集合"""
    collection_name = "futures_index_ccidx"
    display_name = "中证商品指数"


if __name__ == "__main__":
    test = TestFuturesIndexCcidxCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
