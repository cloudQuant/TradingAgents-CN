"""中金所上证50指数日频行情测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionCffexSz50DailySina(OptionsCollectionTestBase):
    """中金所上证50指数日频行情测试类"""
    collection_name = "option_cffex_sz50_daily_sina"
    display_name = "中金所上证50指数日频行情"
    provider_class_name = "OptionCffexSz50DailySinaProvider"
    service_class_name = "OptionCffexSz50DailySinaService"
    is_simple_provider = False
    required_params = ["symbol"]

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_cffex_sz50_daily_sina",
        display_name="中金所上证50指数日频行情",
        params={'symbol': 'ho2512C2500'},
        wait_time=10,
        expected_min_count=50
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        asyncio.run(test_api_update())
    else:
        unittest.main()