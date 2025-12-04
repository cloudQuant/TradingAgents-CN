"""上海期货交易所-库存数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesStockShfeJsCollection(FuturesCollectionTestBase):
    """测试上海期货交易所-库存数据集合"""
    collection_name = "futures_stock_shfe_js"
    display_name = "上海期货交易所-库存数据"


if __name__ == "__main__":
    test = TestFuturesStockShfeJsCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
