#!/usr/bin/env python
"""
测试所有期权数据集合的API刷新功能
逐个测试每个接口，记录结果
"""
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from test_api_base import APITestBase, check_server_running

# 所有集合配置
COLLECTIONS = [
    # 1. 无参数集合
    {"name": "option_contract_info_ctp", "display": "openctp期权合约信息", "params": {}, "expected_min": 1000},
    {"name": "option_current_day_sse", "display": "上交所当日合约", "params": {}, "expected_min": 100},
    {"name": "option_current_day_szse", "display": "深交所当日合约", "params": {}, "expected_min": 100},
    {"name": "option_cffex_sz50_list_sina", "display": "中金所上证50指数合约列表", "params": {}, "expected_min": 1},
    {"name": "option_cffex_hs300_list_sina", "display": "中金所沪深300指数合约列表", "params": {}, "expected_min": 1},
    {"name": "option_cffex_zz1000_list_sina", "display": "中金所中证1000指数合约列表", "params": {}, "expected_min": 1},
    {"name": "option_current_em", "display": "东财期权实时行情", "params": {}, "expected_min": 0},  # 可能被限制
    {"name": "option_value_analysis_em", "display": "东财期权价值分析", "params": {}, "expected_min": 0},
    {"name": "option_risk_analysis_em", "display": "东财期权风险分析", "params": {}, "expected_min": 0},
    {"name": "option_premium_analysis_em", "display": "东财期权溢价分析", "params": {}, "expected_min": 0},
    
    # 2. 带参数集合
    {"name": "option_finance_board", "display": "金融期权行情数据", 
     "params": {"symbol": "华夏上证50ETF期权", "end_month": "2512"}, "expected_min": 10},
    {"name": "option_risk_indicator_sse", "display": "上交所期权风险指标", 
     "params": {"date": "20241210"}, "expected_min": 100},
    {"name": "option_daily_stats_sse", "display": "上交所每日统计", 
     "params": {"date": "20241210"}, "expected_min": 1},
    {"name": "option_daily_stats_szse", "display": "深交所日度概况", 
     "params": {"date": "20241210"}, "expected_min": 1},
    {"name": "option_cffex_sz50_spot_sina", "display": "中金所上证50指数实时行情", 
     "params": {"symbol": "ho2512"}, "expected_min": 10},
    {"name": "option_cffex_hs300_spot_sina", "display": "中金所沪深300指数实时行情", 
     "params": {"symbol": "io2512"}, "expected_min": 10},
    {"name": "option_cffex_zz1000_spot_sina", "display": "中金所中证1000指数实时行情", 
     "params": {"symbol": "mo2512"}, "expected_min": 10},
    {"name": "option_cffex_sz50_daily_sina", "display": "中金所上证50指数日频行情", 
     "params": {"symbol": "ho2512C2500"}, "expected_min": 10},
    {"name": "option_cffex_hs300_daily_sina", "display": "中金所沪深300指数日频行情", 
     "params": {"symbol": "io2512C4000"}, "expected_min": 10},
    {"name": "option_cffex_zz1000_daily_sina", "display": "中金所中证1000指数日频行情", 
     "params": {"symbol": "mo2512C4900"}, "expected_min": 10},
    {"name": "option_sse_list_sina", "display": "上交所50ETF合约到期月份列表", 
     "params": {"symbol": "50ETF", "exchange": "null"}, "expected_min": 1},
    {"name": "option_sse_expire_day_sina", "display": "剩余到期时间", 
     "params": {"trade_date": "202512", "symbol": "50ETF", "exchange": "null"}, "expected_min": 1},
    {"name": "option_sse_codes_sina", "display": "看涨看跌合约代码", 
     "params": {"trade_date": "202512", "underlying": "510050"}, "expected_min": 1},
    {"name": "option_sse_underlying_spot_price_sina", "display": "期权标的物实时数据", 
     "params": {"symbol": "sh510050"}, "expected_min": 1},
    {"name": "option_sse_greeks_sina", "display": "期权希腊字母信息表", 
     "params": {"symbol": "10008573"}, "expected_min": 1},
    {"name": "option_sse_daily_sina", "display": "期权日数据", 
     "params": {"symbol": "10008573"}, "expected_min": 1},
    {"name": "option_lhb_em", "display": "期权龙虎榜", 
     "params": {"symbol": "510050", "indicator": "期权交易情况-认购交易量", "trade_date": "20241210"}, "expected_min": 1},
    {"name": "option_commodity_contract_sina", "display": "商品期权当前合约", 
     "params": {"symbol": "黄金期权"}, "expected_min": 1},
    {"name": "option_commodity_contract_table_sina", "display": "商品期权T型报价表", 
     "params": {"symbol": "黄金期权", "contract": "au2602"}, "expected_min": 1},
    {"name": "option_commodity_hist_sina", "display": "商品期权历史行情", 
     "params": {"symbol": "au2602C608"}, "expected_min": 1},
    {"name": "option_comm_info", "display": "商品期权手续费", 
     "params": {"symbol": "工业硅期权"}, "expected_min": 1},
    {"name": "option_margin", "display": "期权保证金", 
     "params": {"symbol": "原油期权"}, "expected_min": 1},
    {"name": "option_hist_shfe", "display": "上期所期权数据", 
     "params": {"symbol": "铜期权", "date": "20241210"}, "expected_min": 1},
    {"name": "option_hist_dce", "display": "大商所期权数据", 
     "params": {"symbol": "豆粕期权", "date": "20241210"}, "expected_min": 0},  # 可能有问题
    {"name": "option_hist_czce", "display": "郑商所期权数据", 
     "params": {"symbol": "白糖期权", "date": "20241210"}, "expected_min": 1},
    {"name": "option_hist_gfex", "display": "广期所期权数据", 
     "params": {"symbol": "工业硅", "date": "20241210"}, "expected_min": 1},
    {"name": "option_vol_gfex", "display": "广期所隐含波动率", 
     "params": {"symbol": "工业硅", "date": "20241210"}, "expected_min": 1},
    {"name": "option_czce_hist", "display": "郑商所期权历史行情", 
     "params": {"symbol": "SR", "year": "2024"}, "expected_min": 100},
]


async def test_single_collection(tester: APITestBase, config: dict) -> dict:
    """测试单个集合"""
    name = config["name"]
    display = config["display"]
    params = config["params"]
    expected_min = config["expected_min"]
    
    result = {
        "name": name,
        "display": display,
        "refresh_success": False,
        "refresh_error": "",
        "data_count": 0,
        "data_success": False,
        "test_passed": False
    }
    
    try:
        # 1. 刷新数据
        refresh_result = await tester.refresh_collection(name, params)
        result["refresh_success"] = refresh_result["success"]
        result["refresh_error"] = refresh_result["error"]
        
        if not refresh_result["success"]:
            return result
        
        # 2. 等待数据更新
        for i in range(15):
            await asyncio.sleep(2)
            data_result = await tester.get_collection_data(name)
            if data_result["success"] and data_result["total"] > 0:
                result["data_count"] = data_result["total"]
                result["data_success"] = True
                break
        
        # 3. 判断测试是否通过
        result["test_passed"] = (
            result["refresh_success"] and 
            result["data_success"] and 
            result["data_count"] >= expected_min
        )
        
    except Exception as e:
        result["refresh_error"] = str(e)[:100]
    
    return result


async def main():
    """主函数"""
    if not check_server_running():
        print("错误: 后端服务未运行 (localhost:8000)")
        return
    
    print("=" * 70)
    print("期权数据集合API刷新测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"集合数: {len(COLLECTIONS)}")
    print("=" * 70)
    
    tester = APITestBase()
    await tester.setup()
    
    results = []
    success_count = 0
    fail_count = 0
    
    for i, config in enumerate(COLLECTIONS, 1):
        print(f"\n[{i}/{len(COLLECTIONS)}] {config['display']} ({config['name']})")
        print(f"  参数: {config['params']}")
        
        result = await test_single_collection(tester, config)
        results.append(result)
        
        if result["test_passed"]:
            print(f"  ✓ 通过 (数据量: {result['data_count']})")
            success_count += 1
        else:
            print(f"  ✗ 失败 (刷新: {result['refresh_success']}, 数据: {result['data_count']}, 错误: {result['refresh_error']})")
            fail_count += 1
    
    await tester.teardown()
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"总数: {len(COLLECTIONS)}")
    print(f"通过: {success_count}")
    print(f"失败: {fail_count}")
    print(f"通过率: {success_count/len(COLLECTIONS)*100:.1f}%")
    
    if fail_count > 0:
        print("\n失败的集合:")
        for r in results:
            if not r["test_passed"]:
                print(f"  - {r['name']}: 刷新={r['refresh_success']}, 数据={r['data_count']}, 错误={r['refresh_error']}")
    
    # 保存结果
    report_path = Path(__file__).parent / "api_refresh_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(COLLECTIONS),
            "success": success_count,
            "fail": fail_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
