#!/usr/bin/env python
"""
批量生成/更新测试文件，为每个测试文件添加Playwright自动化测试
"""
import os
import re

# 测试文件配置 - 包含每个接口的类型和默认参数
TEST_CONFIGS = {
    # 无参数接口
    "test_01_futures_fees_info": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
    "test_02_futures_comm_info": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "所有"},
        "skip_refresh": False,
    },
    "test_03_futures_rule": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_04_futures_inventory_99": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "豆一"},
        "skip_refresh": False,
    },
    "test_05_futures_inventory_em": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "A"},
        "skip_refresh": False,
    },
    "test_06_futures_dce_position_rank": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_07_futures_gfex_position_rank": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_08_futures_warehouse_receipt_czce": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},  # AKShare参数名是date
        "skip_refresh": False,
    },
    "test_09_futures_warehouse_receipt_dce": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},  # AKShare参数名是date
        "skip_refresh": False,
    },
    "test_10_futures_shfe_warehouse_receipt": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},  # AKShare参数名是date
        "skip_refresh": False,
    },
    "test_11_futures_gfex_warehouse_receipt": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},  # AKShare参数名是date
        "skip_refresh": False,
    },
    "test_12_futures_to_spot_dce": {
        "api_type": "date_param",
        "default_params": {"date": "202412"},  # YYYYMM格式
        "skip_refresh": False,
    },
    "test_13_futures_to_spot_czce": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_14_futures_to_spot_shfe": {
        "api_type": "date_param",
        "default_params": {"date": "202412"},  # YYYYMM格式
        "skip_refresh": False,
    },
    "test_15_futures_delivery_dce": {
        "api_type": "date_param",
        "default_params": {"date": "202412"},
        "skip_refresh": False,
    },
    "test_16_futures_delivery_czce": {
        "api_type": "date_param",
        "default_params": {"date": "202412"},
        "skip_refresh": False,
    },
    "test_17_futures_delivery_shfe": {
        "api_type": "date_param",
        "default_params": {"date": "202412"},
        "skip_refresh": False,
    },
    "test_18_futures_delivery_match_dce": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "a"},  # AKShare参数是symbol
        "skip_refresh": False,
    },
    "test_19_futures_delivery_match_czce": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "PTA"},  # AKShare参数是symbol
        "skip_refresh": False,
    },
    "test_20_futures_stock_shfe_js": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": True,  # 不支持刷新操作
    },
    "test_21_futures_hold_pos_sina": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "成交量", "contract": "IF2501", "date": "20241213"},
        "skip_refresh": False,
    },
    "test_22_futures_spot_sys": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "铜"},
        "skip_refresh": False,
    },
    "test_23_futures_contract_info_shfe": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_24_futures_contract_info_ine": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_25_futures_contract_info_dce": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
    "test_26_futures_contract_info_czce": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_27_futures_contract_info_gfex": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
    "test_28_futures_contract_info_cffex": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_29_futures_zh_spot": {
        "api_type": "no_param",
        "default_params": {},  # 无参数接口
        "skip_refresh": False,
    },
    "test_30_futures_zh_realtime": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "白糖"},
        "skip_refresh": False,
    },
    "test_31_futures_zh_minute_sina": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "IF2501"},
        "skip_refresh": False,
    },
    "test_32_futures_hist_em": {
        "api_type": "date_range_param",
        "default_params": {"symbol": "螺纹钢主力", "period": "daily", "start_date": "20241201", "end_date": "20241213"},
        "skip_refresh": False,
    },
    "test_33_futures_zh_daily_sina": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "RB0"},
        "skip_refresh": False,
    },
    "test_34_get_futures_daily": {
        "api_type": "date_range_param",
        "default_params": {"start_date": "20241201", "end_date": "20241213", "market": "SHFE"},
        "skip_refresh": False,
    },
    "test_35_futures_hq_subscribe_exchange_symbol": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
    "test_36_futures_foreign_commodity_realtime": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "CL"},  # 使用外盘代码
        "skip_refresh": False,
    },
    "test_37_futures_global_spot_em": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
    "test_38_futures_global_hist_em": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "伦敦金"},
        "skip_refresh": False,
    },
    "test_39_futures_foreign_hist": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "GC"},
        "skip_refresh": False,
    },
    "test_40_futures_foreign_detail": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "GC"},
        "skip_refresh": False,
    },
    "test_41_futures_settlement_price_sgx": {
        "api_type": "date_param",
        "default_params": {"date": "20241213"},
        "skip_refresh": False,
    },
    "test_42_futures_main_sina": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "V0"},
        "skip_refresh": False,
    },
    "test_43_futures_contract_detail": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "V2501"},
        "skip_refresh": False,
    },
    "test_44_futures_contract_detail_em": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "螺纹钢主力"},
        "skip_refresh": False,
    },
    "test_45_futures_index_ccidx": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "中证商品期货指数"},
        "skip_refresh": False,
    },
    "test_46_futures_spot_stock": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "铜"},
        "skip_refresh": False,
    },
    "test_47_futures_comex_inventory": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "黄金"},
        "skip_refresh": False,
    },
    "test_48_futures_hog_core": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "全国"},
        "skip_refresh": False,
    },
    "test_49_futures_hog_cost": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "全国"},
        "skip_refresh": False,
    },
    "test_50_futures_hog_supply": {
        "api_type": "symbol_param",
        "default_params": {"symbol": "全国"},
        "skip_refresh": False,
    },
    "test_51_index_hog_spot_price": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
    "test_52_futures_news_shmet": {
        "api_type": "no_param",
        "default_params": {},
        "skip_refresh": False,
    },
}


def update_test_file(filepath: str, config: dict) -> bool:
    """更新测试文件，添加Playwright测试"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有PlaywrightAPITestMixin
    if 'PlaywrightAPITestMixin' in content:
        print(f"  [SKIP] {filepath} 已包含Playwright测试")
        return False
    
    # 1. 更新导入语句
    old_import = "from test_base import FuturesCollectionTestBase"
    new_import = "from test_base import FuturesCollectionTestBase, PlaywrightAPITestMixin, PLAYWRIGHT_AVAILABLE"
    content = content.replace(old_import, new_import)
    
    # 2. 更新类继承
    # 匹配 class TestXxxCollection(FuturesCollectionTestBase):
    class_pattern = r'class (Test\w+Collection)\(FuturesCollectionTestBase\):'
    class_match = re.search(class_pattern, content)
    if class_match:
        class_name = class_match.group(1)
        old_class = f"class {class_name}(FuturesCollectionTestBase):"
        new_class = f"class {class_name}(FuturesCollectionTestBase, PlaywrightAPITestMixin):"
        content = content.replace(old_class, new_class)
    
    # 3. 添加default_params属性（在api_type后面）
    api_type = config['api_type']
    default_params = config['default_params']
    skip_refresh = config.get('skip_refresh', False)
    
    # 查找api_type行并在其后添加default_params
    api_type_pattern = r'(    api_type = "[^"]+"\n    akshare_func = "[^"]+")'
    api_type_match = re.search(api_type_pattern, content)
    if api_type_match:
        old_attrs = api_type_match.group(1)
        new_attrs = old_attrs + f'\n    default_params = {repr(default_params)}'
        if skip_refresh:
            new_attrs += '\n    skip_refresh = True  # 不支持刷新操作'
        content = content.replace(old_attrs, new_attrs)
    
    # 4. 添加test_playwright_api_update方法（在test_akshare_interface后面）
    playwright_test = generate_playwright_test(api_type, default_params, skip_refresh)
    
    # 在test_akshare_interface方法后添加
    akshare_end_pattern = r'(            print\(f"\[OK\] AKShare接口可用"\)\n        except Exception as e:\n            print\(f"  \[WARN\] AKShare接口测试失败: \{e\}"\))'
    if re.search(akshare_end_pattern, content):
        content = re.sub(
            akshare_end_pattern,
            r'\1' + '\n' + playwright_test,
            content
        )
    
    # 5. 更新main函数，添加--playwright参数
    old_main = '''if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", action="store_true", help="包含API功能测试")
    parser.add_argument("--akshare", action="store_true", help="测试AKShare接口")
    args = parser.parse_args()
    
    test = '''
    
    new_main_template = '''if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", action="store_true", help="包含API功能测试")
    parser.add_argument("--akshare", action="store_true", help="测试AKShare接口")
    parser.add_argument("--playwright", action="store_true", help="运行Playwright自动化测试")
    args = parser.parse_args()
    
    test = '''
    
    content = content.replace(old_main, new_main_template)
    
    # 更新测试运行部分
    old_run = '''    if args.akshare:
        test.test_akshare_interface()
    
    success = test.run_all_tests(include_api_tests=args.api)'''
    
    new_run = '''    if args.akshare:
        test.test_akshare_interface()
    
    if args.playwright:
        test.test_playwright_api_update()
    
    success = test.run_all_tests(include_api_tests=args.api)'''
    
    content = content.replace(old_run, new_run)
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  [OK] {filepath} 已更新")
    return True


def generate_playwright_test(api_type: str, default_params: dict, skip_refresh: bool) -> str:
    """生成Playwright测试方法代码"""
    if skip_refresh:
        return '''
    def test_playwright_api_update(self):
        """测试API更新功能（Playwright自动化测试）- 此接口不支持刷新"""
        print("  [SKIP] 此接口不支持刷新操作")
'''
    
    params_str = repr(default_params)
    
    return f'''
    async def test_api_update_async(self):
        """测试API更新功能（异步版本）"""
        if not await self._setup_playwright():
            return {{"success": False, "error": "Playwright未安装"}}
        
        try:
            # 登录
            if not await self._login():
                return {{"success": False, "error": "登录失败"}}
            
            # 构建请求数据
            data = {{
                "update_type": "single",
                "params": {params_str}
            }}
            
            result = await self._api_request_with_auth(
                f"/collections/{{self.collection_name}}/refresh",
                method="POST",
                data=data
            )
            
            return result
            
        finally:
            await self._teardown_playwright()
'''


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="批量更新测试文件")
    parser.add_argument("--dry-run", action="store_true", help="只显示将要更新的文件，不实际修改")
    parser.add_argument("--file", type=str, help="只更新指定的文件")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    updated = 0
    skipped = 0
    
    for test_name, config in TEST_CONFIGS.items():
        filepath = os.path.join(script_dir, f"{test_name}.py")
        
        if args.file and test_name != args.file:
            continue
        
        if not os.path.exists(filepath):
            print(f"  [WARN] 文件不存在: {filepath}")
            continue
        
        if args.dry_run:
            print(f"  [DRY-RUN] 将更新: {filepath}")
            updated += 1
        else:
            if update_test_file(filepath, config):
                updated += 1
            else:
                skipped += 1
    
    print(f"\n更新完成: {updated} 个文件已更新, {skipped} 个文件已跳过")


if __name__ == "__main__":
    main()
