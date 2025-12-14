#!/usr/bin/env python
"""
详细测试每个期货数据集合的AKShare接口
不依赖服务器，直接测试akshare接口是否可用
"""
import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(__file__))

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("[ERROR] AKShare未安装")
    sys.exit(1)

# 所有接口的测试配置
TEST_CONFIGS = [
    # 无参数接口
    {"name": "futures_fees_info", "display": "期货交易费用参照表", "func": "futures_fees_info", "params": {}, "type": "no_param"},
    {"name": "futures_contract_info_dce", "display": "大连商品交易所合约信息", "func": "futures_contract_info_dce", "params": {}, "type": "no_param"},
    {"name": "futures_contract_info_gfex", "display": "广州期货交易所合约信息", "func": "futures_contract_info_gfex", "params": {}, "type": "no_param"},
    {"name": "futures_hq_subscribe_exchange_symbol", "display": "外盘品种代码表", "func": "futures_hq_subscribe_exchange_symbol", "params": {}, "type": "no_param"},
    {"name": "futures_global_spot_em", "display": "外盘实时行情数据-东财", "func": "futures_global_spot_em", "params": {}, "type": "no_param"},
    {"name": "index_hog_spot_price", "display": "生猪市场价格指数", "func": "index_hog_spot_price", "params": {}, "type": "no_param"},
    {"name": "futures_news_shmet", "display": "期货资讯", "func": "futures_news_shmet", "params": {}, "type": "no_param"},
    {"name": "futures_stock_shfe_js", "display": "上海期货交易所-库存数据", "func": "futures_stock_shfe_js", "params": {}, "type": "no_param"},
    
    # 日期参数接口
    {"name": "futures_rule", "display": "期货规则-交易日历表", "func": "futures_rule", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_dce_position_rank", "display": "大连商品交易所-持仓排名", "func": "futures_dce_position_rank", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_gfex_position_rank", "display": "广州期货交易所-持仓排名", "func": "futures_gfex_position_rank", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_warehouse_receipt_czce", "display": "仓单日报-郑州商品交易所", "func": "futures_warehouse_receipt_czce", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_warehouse_receipt_dce", "display": "仓单日报-大连商品交易所", "func": "futures_warehouse_receipt_dce", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_shfe_warehouse_receipt", "display": "仓单日报-上海期货交易所", "func": "futures_shfe_warehouse_receipt", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_gfex_warehouse_receipt", "display": "仓单日报-广州期货交易所", "func": "futures_gfex_warehouse_receipt", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_shfe", "display": "上海期货交易所-合约信息", "func": "futures_contract_info_shfe", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_ine", "display": "上海国际能源交易中心-合约信息", "func": "futures_contract_info_ine", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_czce", "display": "郑州商品交易所-合约信息", "func": "futures_contract_info_czce", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_cffex", "display": "中国金融期货交易所-合约信息", "func": "futures_contract_info_cffex", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_to_spot_dce", "display": "期转现-大连", "func": "futures_to_spot_dce", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_to_spot_czce", "display": "期转现-郑州", "func": "futures_to_spot_czce", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_to_spot_shfe", "display": "期转现-上海", "func": "futures_to_spot_shfe", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_dce", "display": "交割信息-大连", "func": "futures_delivery_dce", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_czce", "display": "交割信息-郑州", "func": "futures_delivery_czce", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_shfe", "display": "交割信息-上海", "func": "futures_delivery_shfe", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_match_dce", "display": "交割配对-大连", "func": "futures_delivery_match_dce", "params": {"symbol": "a"}, "type": "symbol_param"},
    {"name": "futures_delivery_match_czce", "display": "交割配对-郑州", "func": "futures_delivery_match_czce", "params": {"symbol": "PTA"}, "type": "symbol_param"},
    {"name": "futures_settlement_price_sgx", "display": "新加坡交易所期货-结算价", "func": "futures_settlement_price_sgx", "params": {"date": "20241213"}, "type": "date_param"},
    
    # Symbol参数接口
    {"name": "futures_comm_info", "display": "期货手续费与保证金", "func": "futures_comm_info", "params": {"symbol": "所有"}, "type": "symbol_param"},
    {"name": "futures_inventory_99", "display": "库存数据-99期货网", "func": "futures_inventory_99", "params": {"symbol": "豆一"}, "type": "symbol_param"},
    {"name": "futures_inventory_em", "display": "库存数据-东方财富", "func": "futures_inventory_em", "params": {"symbol": "A"}, "type": "symbol_param"},
    {"name": "futures_hold_pos_sina", "display": "持仓数据-新浪", "func": "futures_hold_pos_sina", "params": {"symbol": "成交量", "contract": "IF2501", "date": "20241213"}, "type": "symbol_param"},
    {"name": "futures_spot_sys", "display": "现期图", "func": "futures_spot_sys", "params": {"symbol": "铜"}, "type": "symbol_param"},
    {"name": "futures_zh_spot", "display": "内盘-实时行情数据", "func": "futures_zh_spot", "params": {}, "type": "no_param"},
    {"name": "futures_zh_realtime", "display": "内盘-实时行情数据(品种)", "func": "futures_zh_realtime", "params": {"symbol": "白糖"}, "type": "symbol_param"},
    {"name": "futures_zh_minute_sina", "display": "内盘-分钟数据", "func": "futures_zh_minute_sina", "params": {"symbol": "IF2501"}, "type": "symbol_param"},
    {"name": "futures_zh_daily_sina", "display": "内盘-日线数据", "func": "futures_zh_daily_sina", "params": {"symbol": "RB0"}, "type": "symbol_param"},
    {"name": "futures_main_sina", "display": "期货连续合约-新浪", "func": "futures_main_sina", "params": {"symbol": "V0"}, "type": "symbol_param"},
    {"name": "futures_contract_detail", "display": "期货合约详情-新浪", "func": "futures_contract_detail", "params": {"symbol": "V2501"}, "type": "symbol_param"},
    {"name": "futures_contract_detail_em", "display": "期货合约详情-东财", "func": "futures_contract_detail_em", "params": {"symbol": "螺纹钢主力"}, "type": "symbol_param"},
    {"name": "futures_foreign_commodity_realtime", "display": "外盘-实时行情", "func": "futures_foreign_commodity_realtime", "params": {"symbol": "CL"}, "type": "symbol_param"},
    {"name": "futures_global_hist_em", "display": "外盘-历史行情-东财", "func": "futures_global_hist_em", "params": {"symbol": "伦敦金"}, "type": "symbol_param"},
    {"name": "futures_foreign_hist", "display": "外盘-历史行情", "func": "futures_foreign_hist", "params": {"symbol": "GC"}, "type": "symbol_param"},
    {"name": "futures_foreign_detail", "display": "外盘-合约详情", "func": "futures_foreign_detail", "params": {"symbol": "GC"}, "type": "symbol_param"},
    {"name": "futures_index_ccidx", "display": "中证商品指数", "func": "futures_index_ccidx", "params": {"symbol": "中证商品期货指数"}, "type": "symbol_param"},
    {"name": "futures_spot_stock", "display": "现货库存", "func": "futures_spot_stock", "params": {"symbol": "铜"}, "type": "symbol_param"},
    {"name": "futures_comex_inventory", "display": "COMEX库存数据", "func": "futures_comex_inventory", "params": {"symbol": "黄金"}, "type": "symbol_param"},
    {"name": "futures_hog_core", "display": "生猪核心数据", "func": "futures_hog_core", "params": {"symbol": "全国"}, "type": "symbol_param"},
    {"name": "futures_hog_cost", "display": "生猪成本数据", "func": "futures_hog_cost", "params": {"symbol": "全国"}, "type": "symbol_param"},
    {"name": "futures_hog_supply", "display": "生猪供应数据", "func": "futures_hog_supply", "params": {"symbol": "全国"}, "type": "symbol_param"},
    
    # 日期范围参数接口
    {"name": "futures_hist_em", "display": "内盘-历史行情-东财", "func": "futures_hist_em", "params": {"symbol": "螺纹钢主力", "period": "daily", "start_date": "20241201", "end_date": "20241213"}, "type": "date_range_param"},
    {"name": "get_futures_daily", "display": "内盘-历史行情-交易所", "func": "get_futures_daily", "params": {"start_date": "20241201", "end_date": "20241213", "market": "SHFE"}, "type": "date_range_param"},
]


def test_akshare_interface(config: Dict) -> Dict[str, Any]:
    """测试单个AKShare接口"""
    name = config["name"]
    display = config["display"]
    func_name = config["func"]
    params = config["params"]
    
    result = {
        "name": name,
        "display": display,
        "func": func_name,
        "params": params,
        "type": config["type"],
        "success": False,
        "data_count": 0,
        "columns": [],
        "error": None,
        "duration_ms": 0
    }
    
    start_time = time.time()
    
    try:
        # 获取akshare函数
        if not hasattr(ak, func_name):
            result["error"] = f"AKShare中不存在函数: {func_name}"
            return result
        
        func = getattr(ak, func_name)
        
        # 调用函数
        if params:
            df = func(**params)
        else:
            df = func()
        
        result["duration_ms"] = (time.time() - start_time) * 1000
        
        # 检查结果
        if df is None:
            result["error"] = "返回None"
        elif hasattr(df, 'empty') and df.empty:
            result["success"] = True
            result["data_count"] = 0
            result["columns"] = list(df.columns) if hasattr(df, 'columns') else []
            result["warning"] = "返回空DataFrame"
        elif hasattr(df, '__len__'):
            result["success"] = True
            result["data_count"] = len(df)
            result["columns"] = list(df.columns) if hasattr(df, 'columns') else []
        else:
            result["success"] = True
            result["data_count"] = 1
            
    except Exception as e:
        result["duration_ms"] = (time.time() - start_time) * 1000
        result["error"] = str(e)
    
    return result


def run_all_tests(configs: List[Dict] = None) -> List[Dict]:
    """运行所有测试"""
    if configs is None:
        configs = TEST_CONFIGS
    
    results = []
    total = len(configs)
    
    for i, config in enumerate(configs, 1):
        name = config["name"]
        display = config["display"]
        print(f"[{i}/{total}] 测试 {display} ({name})...", end=" ", flush=True)
        
        result = test_akshare_interface(config)
        results.append(result)
        
        # 打印结果
        if result["success"]:
            if result.get("warning"):
                print(f"[WARN] {result['warning']} ({result['duration_ms']:.0f}ms)")
            else:
                print(f"[OK] {result['data_count']}条数据 ({result['duration_ms']:.0f}ms)")
        else:
            print(f"[FAILED] {result['error'][:60]}")
        
        # 短暂延迟避免请求过快
        time.sleep(0.3)
    
    return results


def print_summary(results: List[Dict]):
    """打印测试汇总"""
    passed = sum(1 for r in results if r["success"] and not r.get("warning"))
    warned = sum(1 for r in results if r["success"] and r.get("warning"))
    failed = sum(1 for r in results if not r["success"])
    
    print("\n" + "="*70)
    print("AKShare接口测试结果汇总")
    print("="*70)
    print(f"通过: {passed}")
    print(f"警告(空数据): {warned}")
    print(f"失败: {failed}")
    print(f"总计: {len(results)}")
    
    if warned > 0:
        print("\n返回空数据的接口:")
        for r in results:
            if r["success"] and r.get("warning"):
                print(f"  - {r['display']} ({r['name']})")
    
    if failed > 0:
        print("\n失败的接口:")
        for r in results:
            if not r["success"]:
                print(f"  - {r['display']} ({r['name']})")
                print(f"      错误: {r['error']}")
    
    print("="*70)


def save_results(results: List[Dict], filepath: str = "akshare_test_results.json"):
    """保存测试结果"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n测试结果已保存到: {filepath}")


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="详细测试AKShare期货接口")
    parser.add_argument("--name", type=str, help="只测试指定的集合")
    parser.add_argument("--type", type=str, choices=["no_param", "date_param", "symbol_param", "date_range_param"], help="只测试指定类型的接口")
    parser.add_argument("--save", action="store_true", help="保存测试结果到文件")
    args = parser.parse_args()
    
    # 过滤测试配置
    configs = TEST_CONFIGS
    if args.name:
        configs = [c for c in configs if c["name"] == args.name]
    if args.type:
        configs = [c for c in configs if c["type"] == args.type]
    
    if not configs:
        print("没有匹配的测试配置")
        return 1
    
    print("="*70)
    print("AKShare期货接口详细测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试数量: {len(configs)}")
    print("="*70 + "\n")
    
    results = run_all_tests(configs)
    print_summary(results)
    
    if args.save:
        save_results(results)
    
    # 返回失败数量
    failed = sum(1 for r in results if not r["success"])
    return failed


if __name__ == "__main__":
    sys.exit(main())
