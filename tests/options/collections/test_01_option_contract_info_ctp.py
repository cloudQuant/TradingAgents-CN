"""openctp期权合约信息测试"""
import unittest
import asyncio
from test_base import OptionsCollectionTestBase
from test_api_base import run_api_test, check_server_running


class TestOptionContractInfoCtp(OptionsCollectionTestBase):
    """openctp期权合约信息测试类"""
    collection_name = "option_contract_info_ctp"
    display_name = "openctp期权合约信息"
    provider_class_name = "OptionContractInfoCtpProvider"
    service_class_name = "OptionContractInfoCtpService"
    is_simple_provider = True


async def test_api_update():
    """测试API更新功能"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return None
    
    result = await run_api_test(
        collection_name="option_contract_info_ctp",
        display_name="openctp期权合约信息",
        params={},  # 无参数接口
        wait_time=30,  # 增加等待时间
        expected_min_count=1000  # 期望至少1000条数据
    )
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        # 运行API测试
        asyncio.run(test_api_update())
    else:
        # 运行单元测试
        unittest.main()
