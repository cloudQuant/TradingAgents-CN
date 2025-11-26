"""
测试 BaseProvider 和 BaseService 基类

验证：
1. 基类可以正常导入
2. 子类可以正常继承
3. 核心方法可以正常调用
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_imports():
    """测试导入"""
    print("=" * 60)
    print("测试1: 导入基类")
    print("=" * 60)
    
    try:
        from app.services.data_sources.base_provider import BaseProvider, SimpleProvider
        print("[OK] BaseProvider 导入成功")
        print("[OK] SimpleProvider 导入成功")
        
        from app.services.data_sources.base_service import BaseService, SimpleService
        print("[OK] BaseService 导入成功")
        print("[OK] SimpleService 导入成功")
        
        return True
    except Exception as e:
        print(f"[FAIL] 导入失败: {e}")
        return False


def test_provider_v2():
    """测试 Provider V2 示例"""
    print("\n" + "=" * 60)
    print("测试2: Provider V2 示例")
    print("=" * 60)
    
    try:
        from app.services.data_sources.funds.providers.fund_name_em_provider_v2 import FundNameEmProviderV2
        
        provider = FundNameEmProviderV2()
        
        assert provider.collection_name == "fund_name_em"
        print(f"[OK] collection_name: {provider.collection_name}")
        
        assert provider.akshare_func == "fund_name_em"
        print(f"[OK] akshare_func: {provider.akshare_func}")
        
        assert provider.unique_keys == ["基金代码"]
        print(f"[OK] unique_keys: {provider.unique_keys}")
        
        field_info = provider.get_field_info()
        assert len(field_info) > 0
        print(f"[OK] field_info 包含 {len(field_info)} 个字段")
        
        return True
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complex_provider_v2():
    """测试复杂 Provider V2 示例"""
    print("\n" + "=" * 60)
    print("测试3: 复杂 Provider V2 示例 (fund_portfolio_hold_em)")
    print("=" * 60)
    
    try:
        from app.services.data_sources.funds.providers.fund_portfolio_hold_em_provider_v2 import FundPortfolioHoldEmProviderV2
        
        provider = FundPortfolioHoldEmProviderV2()
        
        assert provider.collection_name == "fund_portfolio_hold_em"
        print(f"[OK] collection_name: {provider.collection_name}")
        
        assert provider.required_params == ["symbol", "date"]
        print(f"[OK] required_params: {provider.required_params}")
        
        assert provider.param_mapping == {"fund_code": "symbol", "code": "symbol", "year": "date"}
        print(f"[OK] param_mapping: {provider.param_mapping}")
        
        # 测试参数映射
        mapped = provider._map_params({"fund_code": "000001", "year": "2024"})
        assert mapped == {"symbol": "000001", "date": "2024"}
        print(f"[OK] 参数映射: fund_code->symbol, year->date")
        
        # 测试参数验证
        try:
            provider._validate_params({})
            print("[FAIL] 应该抛出参数验证错误")
            return False
        except ValueError as e:
            print(f"[OK] 参数验证: {e}")
        
        return True
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_service_v2():
    """测试 Service V2 示例"""
    print("\n" + "=" * 60)
    print("测试4: Service V2 示例")
    print("=" * 60)
    
    try:
        from app.services.data_sources.funds.services.fund_name_em_service_v2 import FundNameEmServiceV2
        from app.services.data_sources.funds.providers.fund_name_em_provider_v2 import FundNameEmProviderV2
        
        assert FundNameEmServiceV2.collection_name == "fund_name_em"
        print(f"[OK] collection_name: {FundNameEmServiceV2.collection_name}")
        
        assert FundNameEmServiceV2.provider_class == FundNameEmProviderV2
        print(f"[OK] provider_class: {FundNameEmServiceV2.provider_class.__name__}")
        
        return True
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complex_service_v2():
    """测试复杂 Service V2 示例"""
    print("\n" + "=" * 60)
    print("测试5: 复杂 Service V2 示例 (fund_portfolio_hold_em)")
    print("=" * 60)
    
    try:
        from app.services.data_sources.funds.services.fund_portfolio_hold_em_service_v2 import FundPortfolioHoldEmServiceV2
        
        assert FundPortfolioHoldEmServiceV2.batch_source_collection == "fund_name_em"
        print(f"[OK] batch_source_collection: {FundPortfolioHoldEmServiceV2.batch_source_collection}")
        
        assert FundPortfolioHoldEmServiceV2.batch_use_year == True
        print(f"[OK] batch_use_year: {FundPortfolioHoldEmServiceV2.batch_use_year}")
        
        assert FundPortfolioHoldEmServiceV2.batch_years_range == (2010, None)
        print(f"[OK] batch_years_range: {FundPortfolioHoldEmServiceV2.batch_years_range}")
        
        assert FundPortfolioHoldEmServiceV2.incremental_check_fields == ["基金代码", "季度"]
        print(f"[OK] incremental_check_fields: {FundPortfolioHoldEmServiceV2.incremental_check_fields}")
        
        return True
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_code_comparison():
    """对比新旧代码行数"""
    print("\n" + "=" * 60)
    print("测试6: 代码行数对比")
    print("=" * 60)
    
    base_path = os.path.join(os.path.dirname(__file__), '..', '..')
    
    files = [
        ("funds/providers/fund_name_em_provider.py", "funds/providers/fund_name_em_provider_v2.py"),
        ("funds/services/fund_name_em_service.py", "funds/services/fund_name_em_service_v2.py"),
        ("funds/providers/fund_portfolio_hold_em_provider.py", "funds/providers/fund_portfolio_hold_em_provider_v2.py"),
        ("funds/services/fund_portfolio_hold_em_service.py", "funds/services/fund_portfolio_hold_em_service_v2.py"),
    ]
    
    total_old = 0
    total_new = 0
    
    for old_file, new_file in files:
        old_path = os.path.join(base_path, "app/services/data_sources", old_file)
        new_path = os.path.join(base_path, "app/services/data_sources", new_file)
        
        if os.path.exists(old_path) and os.path.exists(new_path):
            with open(old_path, 'r', encoding='utf-8') as f:
                old_lines = len(f.readlines())
            with open(new_path, 'r', encoding='utf-8') as f:
                new_lines = len(f.readlines())
            
            reduction = ((old_lines - new_lines) / old_lines) * 100
            print(f"  {old_file.split('/')[-1]}: {old_lines}行 -> {new_lines}行 (减少 {reduction:.0f}%)")
            
            total_old += old_lines
            total_new += new_lines
    
    if total_old > 0:
        total_reduction = ((total_old - total_new) / total_old) * 100
        print(f"\n  总计: {total_old}行 -> {total_new}行 (减少 {total_reduction:.0f}%)")
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("BaseProvider 和 BaseService 基类测试")
    print("=" * 60)
    
    results = []
    results.append(("导入测试", test_imports()))
    results.append(("Provider V2", test_provider_v2()))
    results.append(("复杂 Provider V2", test_complex_provider_v2()))
    results.append(("Service V2", test_service_v2()))
    results.append(("复杂 Service V2", test_complex_service_v2()))
    results.append(("代码行数对比", test_code_comparison()))
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")
    
    print(f"\n通过: {passed}/{total}")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
