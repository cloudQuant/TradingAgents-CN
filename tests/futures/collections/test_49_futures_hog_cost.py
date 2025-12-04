"""生猪-成本维度数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesHogCostCollection(FuturesCollectionTestBase):
    """测试生猪-成本维度数据集合"""
    collection_name = "futures_hog_cost"
    display_name = "生猪-成本维度"


if __name__ == "__main__":
    test = TestFuturesHogCostCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
