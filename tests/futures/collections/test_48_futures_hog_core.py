"""生猪-核心数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesHogCoreCollection(FuturesCollectionTestBase):
    """测试生猪-核心数据集合"""
    collection_name = "futures_hog_core"
    display_name = "生猪-核心数据"


if __name__ == "__main__":
    test = TestFuturesHogCoreCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
