#!/usr/bin/env python
"""
期权数据接口数据获取测试
测试每个接口是否能正常获取数据
"""
import sys
from pathlib import Path
import time

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import akshare as ak


def test_all_option_interfaces():
    """测试所有期权数据接口"""
    results = []
    
    # 1. 无参数接口测试
    simple_interfaces = [
        ("option_contract_info_ctp", lambda: ak.option_contract_info_ctp()),
        ("option_current_day_sse", lambda: ak.option_current_day_sse()),
        ("option_current_day_szse", lambda: ak.option_current_day_szse()),
        ("option_cffex_sz50_list_sina", lambda: ak.option_cffex_sz50_list_sina()),
        ("option_cffex_hs300_list_sina", lambda: ak.option_cffex_hs300_list_sina()),
        ("option_cffex_zz1000_list_sina", lambda: ak.option_cffex_zz1000_list_sina()),
        ("option_current_em", lambda: ak.option_current_em()),
        ("option_value_analysis_em", lambda: ak.option_value_analysis_em()),
        ("option_risk_analysis_em", lambda: ak.option_risk_analysis_em()),
        ("option_premium_analysis_em", lambda: ak.option_premium_analysis_em()),
    ]
    
    # 2. 带参数接口测试
    param_interfaces = [
        ("option_finance_board", lambda: ak.option_finance_board(symbol="华夏上证50ETF期权", end_month="2512")),
        ("option_risk_indicator_sse", lambda: ak.option_risk_indicator_sse(date="20241210")),
        ("option_daily_stats_sse", lambda: ak.option_daily_stats_sse(date="20241210")),
        ("option_daily_stats_szse", lambda: ak.option_daily_stats_szse(date="20241210")),
        ("option_cffex_sz50_spot_sina", lambda: ak.option_cffex_sz50_spot_sina(symbol="ho2512")),
        ("option_cffex_hs300_spot_sina", lambda: ak.option_cffex_hs300_spot_sina(symbol="io2512")),
        ("option_cffex_zz1000_spot_sina", lambda: ak.option_cffex_zz1000_spot_sina(symbol="mo2512")),
        ("option_cffex_sz50_daily_sina", lambda: ak.option_cffex_sz50_daily_sina(symbol="ho2512C2500")),
        ("option_cffex_hs300_daily_sina", lambda: ak.option_cffex_hs300_daily_sina(symbol="io2512C4000")),
        ("option_cffex_zz1000_daily_sina", lambda: ak.option_cffex_zz1000_daily_sina(symbol="mo2512C4900")),
        ("option_sse_list_sina", lambda: ak.option_sse_list_sina(symbol="50ETF", exchange="null")),
        ("option_sse_expire_day_sina", lambda: ak.option_sse_expire_day_sina(trade_date="202512", symbol="50ETF", exchange="null")),
        ("option_sse_codes_sina", lambda: ak.option_sse_codes_sina(trade_date="202512", underlying="510050")),
        ("option_sse_spot_price_sina", lambda: ak.option_sse_spot_price_sina(symbol="10008573")),
        ("option_sse_underlying_spot_price_sina", lambda: ak.option_sse_underlying_spot_price_sina(symbol="sh510050")),
        ("option_sse_greeks_sina", lambda: ak.option_sse_greeks_sina(symbol="10008573")),
        ("option_sse_daily_sina", lambda: ak.option_sse_daily_sina(symbol="10008573")),
        ("option_lhb_em", lambda: ak.option_lhb_em(symbol="510050", indicator="期权交易情况-认购交易量", trade_date="20241210")),
        ("option_commodity_contract_sina", lambda: ak.option_commodity_contract_sina(symbol="黄金期权")),
        ("option_commodity_contract_table_sina", lambda: ak.option_commodity_contract_table_sina(symbol="黄金期权", contract="au2602")),
        ("option_commodity_hist_sina", lambda: ak.option_commodity_hist_sina(symbol="au2602C608")),
        ("option_comm_info", lambda: ak.option_comm_info(symbol="工业硅期权")),
        ("option_margin", lambda: ak.option_margin(symbol="原油期权")),
        ("option_hist_shfe", lambda: ak.option_hist_shfe(symbol="铜期权", trade_date="20241210")),
        ("option_hist_dce", lambda: ak.option_hist_dce(symbol="豆粕期权", trade_date="20241210")),
        ("option_hist_czce", lambda: ak.option_hist_czce(symbol="白糖期权", trade_date="20241210")),
        ("option_hist_gfex", lambda: ak.option_hist_gfex(symbol="工业硅", trade_date="20241210")),
        ("option_vol_gfex", lambda: ak.option_vol_gfex(symbol="工业硅", trade_date="20241210")),
        ("option_czce_hist", lambda: ak.option_hist_yearly_czce(symbol="SR", year="2024")),
    ]
    
    all_interfaces = simple_interfaces + param_interfaces
    
    print("=" * 70)
    print("期权数据接口数据获取测试")
    print("=" * 70)
    
    success_count = 0
    fail_count = 0
    
    for name, func in all_interfaces:
        try:
            print(f"\n测试: {name}")
            start_time = time.time()
            result = func()
            elapsed = time.time() - start_time
            
            if result is not None:
                if hasattr(result, '__len__'):
                    print(f"  ✓ 成功! 数据量: {len(result)}, 耗时: {elapsed:.2f}s")
                else:
                    print(f"  ✓ 成功! 结果: {result}, 耗时: {elapsed:.2f}s")
                success_count += 1
                results.append((name, "成功", str(len(result) if hasattr(result, '__len__') else result)))
            else:
                print(f"  ✗ 返回空数据")
                fail_count += 1
                results.append((name, "空数据", ""))
        except Exception as e:
            print(f"  ✗ 失败: {str(e)[:100]}")
            fail_count += 1
            results.append((name, "失败", str(e)[:50]))
        
        # 避免请求过快
        time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"  总测试数: {len(all_interfaces)}")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  成功率: {success_count/len(all_interfaces)*100:.1f}%")
    
    if fail_count > 0:
        print("\n失败的接口:")
        for name, status, msg in results:
            if status != "成功":
                print(f"  - {name}: {status} - {msg}")
    
    return results


if __name__ == "__main__":
    test_all_option_interfaces()
