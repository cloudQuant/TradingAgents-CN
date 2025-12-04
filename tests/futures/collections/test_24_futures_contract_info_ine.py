"""上海国际能源交易中心-合约信息数据集合测试用例"""
from test_base import FuturesCollectionTestBase


class TestFuturesContractInfoIneCollection(FuturesCollectionTestBase):
    """测试上海国际能源交易中心-合约信息数据集合"""
    collection_name = "futures_contract_info_ine"
    display_name = "上海国际能源交易中心-合约信息"


if __name__ == "__main__":
    test = TestFuturesContractInfoIneCollection()
    import sys
    sys.exit(0 if test.run_all_tests() else 1)
