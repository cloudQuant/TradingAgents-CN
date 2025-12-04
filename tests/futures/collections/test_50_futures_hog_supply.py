"""生猪-供应维度数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesHogSupplyCollection(FuturesCollectionTestBase):
    """测试生猪-供应维度数据集合"""
    collection_name = "futures_hog_supply"
    display_name = "生猪-供应维度"


if __name__ == "__main__":
    test = TestFuturesHogSupplyCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
