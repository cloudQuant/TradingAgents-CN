"""仓单日报-广州期货交易所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesGfexWarehouseReceiptCollection(FuturesCollectionTestBase):
    """测试仓单日报-广州期货交易所数据集合"""
    collection_name = "futures_gfex_warehouse_receipt"
    display_name = "仓单日报-广州期货交易所"


if __name__ == "__main__":
    test = TestFuturesGfexWarehouseReceiptCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
