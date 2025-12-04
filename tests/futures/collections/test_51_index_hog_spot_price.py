"""生猪市场价格指数数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestIndexHogSpotPriceCollection(FuturesCollectionTestBase):
    """测试生猪市场价格指数数据集合"""
    collection_name = "index_hog_spot_price"
    display_name = "生猪市场价格指数"


if __name__ == "__main__":
    test = TestIndexHogSpotPriceCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
