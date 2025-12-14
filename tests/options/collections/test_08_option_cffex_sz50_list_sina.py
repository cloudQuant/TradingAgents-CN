"""中金所上证50指数合约列表测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionCffexSz50ListSina(OptionsCollectionTestBase):
    """中金所上证50指数合约列表测试类"""
    collection_name = "option_cffex_sz50_list_sina"
    display_name = "中金所上证50指数合约列表"
    provider_class_name = "OptionCffexSz50ListSinaProvider"
    service_class_name = "OptionCffexSz50ListSinaService"
    is_simple_provider = True

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_cffex_sz50_list_sina",
        display_name="中金所上证50指数合约列表",
        params={},
        wait_time=10,
        expected_min_count=1
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        asyncio.run(test_api_update())
    else:
        unittest.main()