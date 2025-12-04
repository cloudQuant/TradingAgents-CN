"""新加坡交易所期货-结算价数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesSettlementPriceSgxCollection(FuturesCollectionTestBase):
    """测试新加坡交易所期货-结算价数据集合"""
    collection_name = "futures_settlement_price_sgx"
    display_name = "新加坡交易所期货-结算价"


if __name__ == "__main__":
    test = TestFuturesSettlementPriceSgxCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
