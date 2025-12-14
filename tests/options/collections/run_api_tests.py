#!/usr/bin/env python
"""
运行所有期权数据集合的API更新测试
按顺序测试每个集合的刷新功能和数据获取
"""
import sys
import asyncio
import importlib
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from test_api_base import check_server_running


async def run_all_api_tests():
    """运行所有API测试"""
    print("=" * 70)
    print("期权数据集合API更新测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    if not check_server_running():
        print("\n错误: 后端服务未运行 (localhost:8000)")
        print("请先启动后端服务")
        return
    
    # 测试文件列表
    test_files = [
        "test_01_option_contract_info_ctp",
        "test_02_option_finance_board",
        "test_03_option_risk_indicator_sse",
        "test_04_option_current_day_sse",
        "test_05_option_current_day_szse",
        "test_06_option_daily_stats_sse",
        "test_07_option_daily_stats_szse",
        "test_08_option_cffex_sz50_list_sina",
        "test_09_option_cffex_hs300_list_sina",
        "test_10_option_cffex_zz1000_list_sina",
        "test_11_option_cffex_sz50_spot_sina",
        "test_12_option_cffex_hs300_spot_sina",
        "test_13_option_cffex_zz1000_spot_sina",
        "test_14_option_cffex_sz50_daily_sina",
        "test_15_option_cffex_hs300_daily_sina",
        "test_16_option_cffex_zz1000_daily_sina",
        "test_17_option_sse_list_sina",
        "test_18_option_sse_expire_day_sina",
        "test_19_option_sse_codes_sina",
        "test_20_option_sse_spot_price_sina",
        "test_21_option_sse_underlying_spot_price_sina",
        "test_22_option_sse_greeks_sina",
        "test_23_option_sse_minute_sina",
        "test_24_option_sse_daily_sina",
        "test_25_option_finance_minute_sina",
        "test_26_option_minute_em",
        "test_27_option_current_em",
        "test_28_option_lhb_em",
        "test_29_option_value_analysis_em",
        "test_30_option_risk_analysis_em",
        "test_31_option_premium_analysis_em",
        "test_32_option_commodity_contract_sina",
        "test_33_option_commodity_contract_table_sina",
        "test_34_option_commodity_hist_sina",
        "test_35_option_comm_info",
        "test_36_option_margin",
        "test_37_option_hist_shfe",
        "test_38_option_hist_dce",
        "test_39_option_hist_czce",
        "test_40_option_hist_gfex",
        "test_41_option_vol_gfex",
        "test_42_option_czce_hist",
    ]
    
    results = []
    
    for test_file in test_files:
        try:
            module = importlib.import_module(test_file)
            if hasattr(module, 'test_api_update'):
                result = await module.test_api_update()
                if result:
                    results.append(result)
        except Exception as e:
            print(f"\n错误: 运行 {test_file} 失败: {e}")
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    
    if results:
        passed = sum(1 for r in results if r.get("test_passed", False))
        failed = len(results) - passed
        
        print(f"总测试数: {len(results)}")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        print(f"通过率: {passed/len(results)*100:.1f}%")
        
        if failed > 0:
            print("\n失败的测试:")
            for r in results:
                if not r.get("test_passed", False):
                    print(f"  - {r['collection_name']}: 刷新={r['refresh_success']}, 数据量={r['data_count']}")


if __name__ == "__main__":
    asyncio.run(run_all_api_tests())
