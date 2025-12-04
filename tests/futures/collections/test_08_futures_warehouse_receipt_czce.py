"""仓单日报-郑州商品交易所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesWarehouseReceiptCzceCollection(FuturesCollectionTestBase):
    """测试仓单日报-郑州商品交易所数据集合"""
    collection_name = "futures_warehouse_receipt_czce"
    display_name = "仓单日报-郑州商品交易所"


if __name__ == "__main__":
    test = TestFuturesWarehouseReceiptCzceCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
