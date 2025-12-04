"""COMEX库存数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesComexInventoryCollection(FuturesCollectionTestBase):
    """测试COMEX库存数据集合"""
    collection_name = "futures_comex_inventory"
    display_name = "COMEX库存数据"


if __name__ == "__main__":
    test = TestFuturesComexInventoryCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
