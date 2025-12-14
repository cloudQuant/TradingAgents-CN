"""商品期权手续费测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionCommInfo(OptionsCollectionTestBase):
    """商品期权手续费测试类"""
    collection_name = "option_comm_info"
    display_name = "商品期权手续费"
    provider_class_name = "OptionCommInfoProvider"
    service_class_name = "OptionCommInfoService"
    is_simple_provider = True

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_comm_info",
        display_name="商品期权手续费",
        params={'symbol': '工业硅期权'},
        wait_time=15,
        expected_min_count=100
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        asyncio.run(test_api_update())
    else:
        unittest.main()