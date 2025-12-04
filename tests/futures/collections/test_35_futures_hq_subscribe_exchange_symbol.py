"""外盘-品种代码表数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesHqSubscribeExchangeSymbolCollection(FuturesCollectionTestBase):
    """测试外盘-品种代码表数据集合"""
    collection_name = "futures_hq_subscribe_exchange_symbol"
    display_name = "外盘-品种代码表"


if __name__ == "__main__":
    test = TestFuturesHqSubscribeExchangeSymbolCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
