"""中金所沪深300指数实时行情测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionCffexHs300SpotSina(OptionsCollectionTestBase):
    """中金所沪深300指数实时行情测试类"""
    collection_name = "option_cffex_hs300_spot_sina"
    display_name = "中金所沪深300指数实时行情"
    provider_class_name = "OptionCffexHs300SpotSinaProvider"
    service_class_name = "OptionCffexHs300SpotSinaService"
    is_simple_provider = False
    required_params = ["symbol"]

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_cffex_hs300_spot_sina",
        display_name="中金所沪深300指数实时行情",
        params={'symbol': 'io2512'},
        wait_time=10,
        expected_min_count=10
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        asyncio.run(test_api_update())
    else:
        unittest.main()