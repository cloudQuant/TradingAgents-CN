"""金融期权行情数据测试"""
import unittest
import asyncio
from test_base import OptionsCollectionTestBase
from test_api_base import run_api_test, check_server_running


class TestOptionFinanceBoard(OptionsCollectionTestBase):
    """金融期权行情数据测试类"""
    collection_name = "option_finance_board"
    display_name = "金融期权行情数据"
    provider_class_name = "OptionFinanceBoardProvider"
    service_class_name = "OptionFinanceBoardService"
    is_simple_provider = False
    required_params = ["symbol", "end_month"]


async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_finance_board",
        display_name="金融期权行情数据",
        params={"symbol": "华夏上证50ETF期权", "end_month": "2512"},
        wait_time=5,
        expected_min_count=10  # 期望至少10条数据
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        asyncio.run(test_api_update())
    else:
        unittest.main()
