"""期货规则-交易日历表数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesRuleCollection(FuturesCollectionTestBase):
    """测试期货规则-交易日历表数据集合"""
    collection_name = "futures_rule"
    display_name = "期货规则-交易日历表"


if __name__ == "__main__":
    test = TestFuturesRuleCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
