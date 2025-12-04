"""期转现-大商所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesToSpotDceCollection(FuturesCollectionTestBase):
    """测试期转现-大商所数据集合"""
    collection_name = "futures_to_spot_dce"
    display_name = "期转现-大商所"


if __name__ == "__main__":
    test = TestFuturesToSpotDceCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
