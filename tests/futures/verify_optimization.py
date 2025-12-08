"""
期货数据集合优化验证脚本

验证服务和配置的正确性
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_config_import():
    """测试配置文件导入"""
    print("\n[1] 测试配置文件导入...")
    try:
        from app.config.futures_update_config import (
            FUTURES_UPDATE_CONFIGS,
            get_futures_collection_update_config,
            get_all_futures_collection_update_configs
        )
        print(f"  [OK] 配置文件导入成功，共 {len(FUTURES_UPDATE_CONFIGS)} 个集合配置")
        return True
    except Exception as e:
        print(f"  [FAIL] 配置文件导入失败: {e}")
        return False


def test_service_imports():
    """测试服务类导入"""
    print("\n[2] 测试服务类导入...")
    
    services_to_test = [
        ("futures_fees_info", "FuturesFeesInfoService"),
        ("futures_dce_position_rank", "FuturesDcePositionRankService"),
        ("futures_gfex_position_rank", "FuturesGfexPositionRankService"),
        ("futures_warehouse_receipt_czce", "FuturesWarehouseReceiptCzceService"),
        ("futures_warehouse_receipt_dce", "FuturesWarehouseReceiptDceService"),
        ("futures_shfe_warehouse_receipt", "FuturesShfeWarehouseReceiptService"),
        ("futures_gfex_warehouse_receipt", "FuturesGfexWarehouseReceiptService"),
        ("get_futures_daily", "GetFuturesDailyService"),
        ("futures_inventory_em", "FuturesInventoryEmService"),
        ("futures_contract_info_dce", "FuturesContractInfoDceService"),
        ("futures_global_spot_em", "FuturesGlobalSpotEmService"),
        ("index_hog_spot_price", "IndexHogSpotPriceService"),
    ]
    
    success_count = 0
    for collection_name, class_name in services_to_test:
        try:
            module_name = f"app.services.data_sources.futures.services.{collection_name}_service"
            module = __import__(module_name, fromlist=[class_name])
            service_class = getattr(module, class_name)
            
            # 检查是否有 provider_class
            if hasattr(service_class, 'provider_class') and service_class.provider_class:
                print(f"  [OK] {class_name} (provider: {service_class.provider_class.__name__})")
            else:
                print(f"  [WARN] {class_name} (no provider_class)")
            
            success_count += 1
        except Exception as e:
            print(f"  [FAIL] {class_name}: {e}")
    
    print(f"\n  导入结果: {success_count}/{len(services_to_test)} 成功")
    return success_count == len(services_to_test)


def test_base_classes():
    """测试基类导入"""
    print("\n[3] 测试基类导入...")
    
    try:
        from app.services.data_sources.futures.services.date_incremental_service import DateIncrementalService
        print("  [OK] DateIncrementalService")
    except Exception as e:
        print(f"  [FAIL] DateIncrementalService: {e}")
        return False
    
    try:
        from app.services.data_sources.futures.services.symbol_batch_service import SymbolBatchService
        print("  [OK] SymbolBatchService")
    except Exception as e:
        print(f"  [FAIL] SymbolBatchService: {e}")
        return False
    
    return True


def test_config_structure():
    """测试配置结构"""
    print("\n[4] 测试配置结构...")
    
    from app.config.futures_update_config import FUTURES_UPDATE_CONFIGS
    
    no_param_collections = []
    date_param_collections = []
    symbol_param_collections = []
    
    for name, config in FUTURES_UPDATE_CONFIGS.items():
        single = config.get("single_update", {})
        batch = config.get("batch_update", {})
        
        # 检查无参数接口
        if single.get("enabled") and not single.get("params") and not batch.get("enabled"):
            no_param_collections.append(name)
        
        # 检查日期参数接口
        elif single.get("params"):
            params = single.get("params", [])
            if any(p.get("name") == "date" for p in params):
                date_param_collections.append(name)
            elif any(p.get("name") == "symbol" for p in params):
                symbol_param_collections.append(name)
    
    print(f"  无参数接口: {len(no_param_collections)} 个")
    for name in no_param_collections[:5]:
        print(f"    - {name}")
    if len(no_param_collections) > 5:
        print(f"    ... 还有 {len(no_param_collections) - 5} 个")
    
    print(f"  日期参数接口: {len(date_param_collections)} 个")
    for name in date_param_collections[:5]:
        print(f"    - {name}")
    if len(date_param_collections) > 5:
        print(f"    ... 还有 {len(date_param_collections) - 5} 个")
    
    print(f"  Symbol参数接口: {len(symbol_param_collections)} 个")
    for name in symbol_param_collections[:5]:
        print(f"    - {name}")
    if len(symbol_param_collections) > 5:
        print(f"    ... 还有 {len(symbol_param_collections) - 5} 个")
    
    return True


def main():
    """运行所有测试"""
    print("=" * 60)
    print("期货数据集合优化验证")
    print("=" * 60)
    
    results = []
    
    results.append(("配置文件导入", test_config_import()))
    results.append(("服务类导入", test_service_imports()))
    results.append(("基类导入", test_base_classes()))
    results.append(("配置结构", test_config_structure()))
    
    print("\n" + "=" * 60)
    print("验证结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False
    
    print("\n" + ("所有测试通过!" if all_passed else "部分测试失败，请检查"))
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
