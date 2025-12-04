#!/usr/bin/env python
"""
运行所有货币数据集合测试
"""
import os
import sys
import unittest
from pathlib import Path
from importlib import import_module
from pkgutil import iter_modules

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def discover_and_run_tests():
    """发现并运行所有测试"""
    tests_dir = Path(__file__).parent
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 发现所有test_*.py文件
    test_files = list(tests_dir.glob("test_*.py"))
    test_files = [f for f in test_files if f.name != "test_base.py"]
    test_files.sort()
    
    print(f"\n发现 {len(test_files)} 个测试文件\n")
    
    # 加载每个测试文件
    for test_file in test_files:
        module_name = test_file.stem
        try:
            module = import_module(f"tests.currencies.collections.{module_name}")
            tests = loader.loadTestsFromModule(module)
            suite.addTests(tests)
            print(f"  ✓ 加载测试: {module_name}")
        except Exception as e:
            print(f"  ✗ 加载失败: {module_name} - {e}")
    
    print("\n" + "=" * 70)
    print("开始运行测试")
    print("=" * 70 + "\n")
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"  运行测试数: {result.testsRun}")
    print(f"  成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败: {len(result.failures)}")
    print(f"  错误: {len(result.errors)}")
    print(f"  跳过: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n出错的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result


def run_quick_check():
    """快速检查所有集合"""
    print("\n" + "=" * 70)
    print("货币数据集合快速检查")
    print("=" * 70 + "\n")
    
    try:
        from app.services.data_sources.currencies import (
            get_currency_collection_definitions,
            get_registered_currency_providers,
            get_registered_currency_services,
        )
        
        definitions = get_currency_collection_definitions()
        providers = get_registered_currency_providers()
        services = get_registered_currency_services()
        
        print(f"集合定义数量: {len(definitions)}")
        print(f"Provider数量: {len(providers)}")
        print(f"Service数量: {len(services)}")
        
        print("\n已注册的集合:")
        for defn in definitions:
            name = defn.get('name', '')
            display_name = defn.get('display_name', '')
            print(f"  - {name}: {display_name}")
        
        # 检查Provider和Service是否匹配
        provider_names = {p.collection_name for p in providers}
        service_names = set(services.keys())
        
        missing_services = provider_names - service_names
        missing_providers = service_names - provider_names
        
        if missing_services:
            print(f"\n⚠️  有Provider但缺少Service的集合: {missing_services}")
        
        if missing_providers:
            print(f"\n⚠️  有Service但缺少Provider的集合: {missing_providers}")
        
        if not missing_services and not missing_providers:
            print("\n✓ 所有Provider和Service都已正确匹配")
        
    except ImportError as e:
        print(f"导入失败: {e}")
        return False
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="运行货币数据集合测试")
    parser.add_argument("--quick", action="store_true", help="只运行快速检查")
    parser.add_argument("--full", action="store_true", help="运行完整测试")
    args = parser.parse_args()
    
    if args.quick:
        run_quick_check()
    elif args.full:
        result = discover_and_run_tests()
        sys.exit(0 if result.wasSuccessful() else 1)
    else:
        # 默认先运行快速检查，再运行完整测试
        run_quick_check()
        print("\n")
        result = discover_and_run_tests()
        sys.exit(0 if result.wasSuccessful() else 1)
