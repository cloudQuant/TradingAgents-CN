"""
验证期货数据集合优化结果
测试每个接口是否能正常获取数据
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def test_interface(name, func, *args, **kwargs):
    """测试单个接口"""
    try:
        result = func(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            if result.empty:
                print(f"  [WARN] {name}: 返回空DataFrame")
                return "warn"
            else:
                print(f"  [OK] {name}: 返回 {len(result)} 行数据")
                return "ok"
        elif isinstance(result, dict):
            if not result:
                print(f"  [WARN] {name}: 返回空字典")
                return "warn"
            else:
                print(f"  [OK] {name}: 返回 {len(result)} 个键")
                return "ok"
        else:
            print(f"  [OK] {name}: 返回 {type(result).__name__}")
            return "ok"
    except Exception as e:
        print(f"  [FAIL] {name}: {str(e)[:100]}")
        return "fail"


def main():
    """主测试函数"""
    print("="*70)
    print("期货数据接口验证")
    print("="*70)
    
    results = {"ok": 0, "warn": 0, "fail": 0}
    
    # 获取测试日期 - 使用已知的交易日
    # 使用固定的历史交易日来避免周末/节假日问题
    recent_date = "20241213"  # 使用一个已知的交易日
    recent_month = "202411"
    
    # 类型1：无参数接口
    print("\n[类型1] 无参数接口")
    print("-"*50)
    
    tests_type1 = [
        ("futures_fees_info", ak.futures_fees_info),
        ("futures_contract_info_dce", ak.futures_contract_info_dce),
        ("futures_contract_info_gfex", ak.futures_contract_info_gfex),
        ("futures_hq_subscribe_exchange_symbol", ak.futures_hq_subscribe_exchange_symbol),
        ("futures_global_spot_em", ak.futures_global_spot_em),
        ("index_hog_spot_price", ak.index_hog_spot_price),
    ]
    
    for name, func in tests_type1:
        r = test_interface(name, func)
        results[r] += 1
    
    # 类型2：日期参数接口
    print("\n[类型2] 日期参数接口")
    print("-"*50)
    
    tests_type2 = [
        ("futures_rule", lambda: ak.futures_rule(date=recent_date)),
        ("futures_dce_position_rank", lambda: ak.futures_dce_position_rank(date=recent_date)),
        ("futures_gfex_position_rank", lambda: ak.futures_gfex_position_rank(date=recent_date)),
        ("futures_warehouse_receipt_czce", lambda: ak.futures_warehouse_receipt_czce(date=recent_date)),
        ("futures_warehouse_receipt_dce", lambda: ak.futures_warehouse_receipt_dce(date=recent_date)),
        ("futures_shfe_warehouse_receipt", lambda: ak.futures_shfe_warehouse_receipt(date=recent_date)),
        ("futures_gfex_warehouse_receipt", lambda: ak.futures_gfex_warehouse_receipt(date=recent_date)),
        ("futures_contract_info_shfe", lambda: ak.futures_contract_info_shfe(date=recent_date)),
        ("futures_contract_info_ine", lambda: ak.futures_contract_info_ine(date=recent_date)),
        ("futures_contract_info_czce", lambda: ak.futures_contract_info_czce(date=recent_date)),
        ("futures_contract_info_cffex", lambda: ak.futures_contract_info_cffex(date=recent_date)),
        ("futures_to_spot_czce", lambda: ak.futures_to_spot_czce(date=recent_date)),
        ("futures_to_spot_dce", lambda: ak.futures_to_spot_dce(date=recent_month)),
        ("futures_to_spot_shfe", lambda: ak.futures_to_spot_shfe(date=recent_month)),
        ("futures_settlement_price_sgx", lambda: ak.futures_settlement_price_sgx(date=recent_date)),
    ]
    
    for name, func in tests_type2:
        r = test_interface(name, func)
        results[r] += 1
    
    # 类型3：交易所/市场选择接口
    print("\n[类型3] 交易所/市场选择接口")
    print("-"*50)
    
    tests_type3 = [
        ("futures_comm_info", lambda: ak.futures_comm_info(symbol="所有")),
        ("futures_zh_spot", lambda: ak.futures_zh_spot(market="CF")),
    ]
    
    for name, func in tests_type3:
        r = test_interface(name, func)
        results[r] += 1
    
    # 类型4：symbol参数接口
    print("\n[类型4] symbol参数接口")
    print("-"*50)
    
    tests_type4 = [
        ("futures_inventory_99", lambda: ak.futures_inventory_99(symbol="豆一")),
        ("futures_inventory_em", lambda: ak.futures_inventory_em(symbol="A")),
        ("futures_spot_sys", lambda: ak.futures_spot_sys(symbol="铜")),
        ("futures_zh_realtime", lambda: ak.futures_zh_realtime(symbol="白糖")),
        ("futures_comex_inventory", lambda: ak.futures_comex_inventory(symbol="黄金")),
        ("futures_index_ccidx", lambda: ak.futures_index_ccidx(symbol="中证商品期货指数")),
        ("futures_spot_stock", lambda: ak.futures_spot_stock(symbol="铜")),
        ("futures_main_sina", lambda: ak.futures_main_sina(symbol="V0")),
        ("futures_contract_detail", lambda: ak.futures_contract_detail(symbol="V2501")),
        ("futures_contract_detail_em", lambda: ak.futures_contract_detail_em(symbol="聚氯乙烯2501")),
        ("futures_foreign_commodity_realtime", lambda: ak.futures_foreign_commodity_realtime(symbol="伦敦金")),
        ("futures_foreign_detail", lambda: ak.futures_foreign_detail(symbol="GC")),
    ]
    
    for name, func in tests_type4:
        r = test_interface(name, func)
        results[r] += 1
    
    # 类型5：历史数据接口
    print("\n[类型5] 历史数据接口")
    print("-"*50)
    
    tests_type5 = [
        ("futures_zh_minute_sina", lambda: ak.futures_zh_minute_sina(symbol="IF2501", period="1")),
        ("futures_zh_daily_sina", lambda: ak.futures_zh_daily_sina(symbol="RB0")),
        ("futures_hist_em", lambda: ak.futures_hist_em(symbol="螺纹钢主力")),
        ("get_futures_daily", lambda: ak.get_futures_daily(start_date="20241201", end_date="20241205", market="SHFE")),
        ("futures_global_hist_em", lambda: ak.futures_global_hist_em(symbol="伦敦金")),
        ("futures_foreign_hist", lambda: ak.futures_foreign_hist(symbol="GC")),
    ]
    
    for name, func in tests_type5:
        r = test_interface(name, func)
        results[r] += 1
    
    # 类型6：生猪数据接口
    print("\n[类型6] 生猪数据接口")
    print("-"*50)
    
    tests_type6 = [
        ("futures_hog_core", lambda: ak.futures_hog_core(symbol="全国")),
        ("futures_hog_cost", lambda: ak.futures_hog_cost(symbol="全国")),
        ("futures_hog_supply", lambda: ak.futures_hog_supply(symbol="全国")),
    ]
    
    for name, func in tests_type6:
        r = test_interface(name, func)
        results[r] += 1
    
    # 类型7：其他接口
    print("\n[类型7] 其他接口")
    print("-"*50)
    
    tests_type7 = [
        ("futures_hold_pos_sina", lambda: ak.futures_hold_pos_sina(symbol="成交量", contract="RB2501", date="20241213")),
        ("futures_stock_shfe_js", lambda: ak.futures_stock_shfe_js()),
        ("futures_news_shmet", lambda: ak.futures_news_shmet()),
    ]
    
    for name, func in tests_type7:
        r = test_interface(name, func)
        results[r] += 1
    
    # 汇总
    print("\n" + "="*70)
    print("测试结果汇总")
    print("="*70)
    total = sum(results.values())
    print(f"成功: {results['ok']}")
    print(f"警告: {results['warn']}")
    print(f"失败: {results['fail']}")
    print(f"总计: {total}")
    print("="*70)
    
    return results['fail'] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
