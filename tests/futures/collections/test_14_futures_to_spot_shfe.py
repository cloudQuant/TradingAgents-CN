"""期转现-上期所数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesToSpotShfeCollection(FuturesCollectionTestBase):
    """测试期转现-上期所数据集合"""
    collection_name = "futures_to_spot_shfe"
    display_name = "期转现-上期所"


if __name__ == "__main__":
    test = TestFuturesToSpotShfeCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
