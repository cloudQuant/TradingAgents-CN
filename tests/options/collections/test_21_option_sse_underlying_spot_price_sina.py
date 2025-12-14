"""期权标的物实时数据测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionSseUnderlyingSpotPriceSina(OptionsCollectionTestBase):
    """期权标的物实时数据测试类"""
    collection_name = "option_sse_underlying_spot_price_sina"
    display_name = "期权标的物实时数据"
    provider_class_name = "OptionSseUnderlyingSpotPriceSinaProvider"
    service_class_name = "OptionSseUnderlyingSpotPriceSinaService"
    is_simple_provider = False
    required_params = ["symbol"]

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_sse_underlying_spot_price_sina",
        display_name="期权标的物实时数据",
        params={'symbol': 'sh510050'},
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