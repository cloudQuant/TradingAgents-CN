"""现货与股票数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesSpotStockCollection(FuturesCollectionTestBase):
    """测试现货与股票数据集合"""
    collection_name = "futures_spot_stock"
    display_name = "现货与股票"


if __name__ == "__main__":
    test = TestFuturesSpotStockCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
