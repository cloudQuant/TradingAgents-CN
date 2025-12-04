"""期货资讯数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesNewsShmetCollection(FuturesCollectionTestBase):
    """测试期货资讯数据集合"""
    collection_name = "futures_news_shmet"
    display_name = "期货资讯"


if __name__ == "__main__":
    test = TestFuturesNewsShmetCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
