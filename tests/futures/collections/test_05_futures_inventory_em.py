"""库存数据-东方财富数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesInventoryEmCollection(FuturesCollectionTestBase):
    """测试库存数据-东方财富数据集合"""
    collection_name = "futures_inventory_em"
    display_name = "库存数据-东方财富"


if __name__ == "__main__":
    test = TestFuturesInventoryEmCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
