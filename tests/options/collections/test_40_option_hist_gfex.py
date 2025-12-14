"""广期所期权数据测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionHistGfex(OptionsCollectionTestBase):
    """广期所期权数据测试类"""
    collection_name = "option_hist_gfex"
    display_name = "广期所期权数据"
    provider_class_name = "OptionHistGfexProvider"
    service_class_name = "OptionHistGfexService"
    is_simple_provider = False
    required_params = ["symbol", "date"]

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_hist_gfex",
        display_name="广期所期权数据",
        params={'symbol': '工业硅', 'date': '20241210'},
        wait_time=10,
        expected_min_count=100
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        asyncio.run(test_api_update())
    else:
        unittest.main()