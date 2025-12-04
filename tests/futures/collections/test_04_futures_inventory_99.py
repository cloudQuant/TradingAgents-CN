"""库存数据-99期货网数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesInventory99Collection(FuturesCollectionTestBase):
    """测试库存数据-99期货网数据集合"""
    collection_name = "futures_inventory_99"
    display_name = "库存数据-99期货网"


if __name__ == "__main__":
    test = TestFuturesInventory99Collection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
