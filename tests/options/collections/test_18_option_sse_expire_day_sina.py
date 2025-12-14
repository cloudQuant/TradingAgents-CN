"""剩余到期时间测试"""
import unittest
import asyncio
from test_api_base import run_api_test, check_server_running
from test_base import OptionsCollectionTestBase


class TestOptionSseExpireDaySina(OptionsCollectionTestBase):
    """剩余到期时间测试类"""
    collection_name = "option_sse_expire_day_sina"
    display_name = "剩余到期时间"
    provider_class_name = "OptionSseExpireDaySinaProvider"
    service_class_name = "OptionSseExpireDaySinaService"
    is_simple_provider = False
    required_params = ["trade_date", "symbol"]

async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_sse_expire_day_sina",
        display_name="剩余到期时间",
        params={'trade_date': '202512', 'symbol': '50ETF', 'exchange': 'null'},
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