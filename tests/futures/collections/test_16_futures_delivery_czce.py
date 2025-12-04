"""交割统计-郑商所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesDeliveryCzceCollection(FuturesCollectionTestBase):
    """测试交割统计-郑商所数据集合"""
    collection_name = "futures_delivery_czce"
    display_name = "交割统计-郑商所"


if __name__ == "__main__":
    test = TestFuturesDeliveryCzceCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
