"""仓单日报-上海期货交易所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesShfeWarehouseReceiptCollection(FuturesCollectionTestBase):
    """测试仓单日报-上海期货交易所数据集合"""
    collection_name = "futures_shfe_warehouse_receipt"
    display_name = "仓单日报-上海期货交易所"


if __name__ == "__main__":
    test = TestFuturesShfeWarehouseReceiptCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
