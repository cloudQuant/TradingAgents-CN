#!/usr/bin/env python
"""
期货数据集合完整测试套件
运行所有测试：基础测试、AKShare接口测试、网站API更新功能测试、Playwright自动化测试
"""
import os
import sys
import asyncio
import argparse
import subprocess
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))


def run_basic_tests(include_akshare: bool = False):
    """运行基础测试"""
    from run_all_tests import run_all_tests
    return run_all_tests(include_api_tests=False, include_akshare_tests=include_akshare)


def run_web_api_tests():
    """运行网站API更新功能测试"""
    try:
        from test_web_api_update import run_web_api_tests as web_tests
        return asyncio.run(web_tests())
    except ImportError as e:
        print(f"[WARN] 无法导入网站API测试模块: {e}")
        return True
    except Exception as e:
        print(f"[ERROR] 网站API测试失败: {e}")
        return False


def run_playwright_tests():
    """运行所有测试文件的Playwright自动化测试"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取所有测试文件
    test_files = sorted([
        f for f in os.listdir(script_dir)
        if f.startswith("test_") and f.endswith(".py") 
        and f not in ["test_base.py", "test_web_api_update.py"]
    ])
    
    passed = 0
    failed = 0
    skipped = 0
    failed_tests = []
    
    print(f"\n共 {len(test_files)} 个测试文件")
    print("-" * 50)
    
    for test_file in test_files:
        test_path = os.path.join(script_dir, test_file)
        test_name = test_file.replace(".py", "").replace("test_", "")
        
        try:
            result = subprocess.run(
                [sys.executable, test_path, "--playwright"],
                capture_output=True,
                text=True,
                timeout=120  # 2分钟超时
            )
            
            output = result.stdout + result.stderr
            
            if "[SKIP]" in output:
                print(f"  [SKIP] {test_name}")
                skipped += 1
            elif result.returncode == 0 and ("[OK]" in output or "SUCCESS" in output):
                print(f"  [OK] {test_name}")
                passed += 1
            else:
                print(f"  [FAILED] {test_name}")
                failed += 1
                failed_tests.append(test_name)
                
        except subprocess.TimeoutExpired:
            print(f"  [TIMEOUT] {test_name}")
            failed += 1
            failed_tests.append(test_name)
        except Exception as e:
            print(f"  [ERROR] {test_name}: {e}")
            failed += 1
            failed_tests.append(test_name)
    
    print("-" * 50)
    print(f"Playwright测试结果: 通过={passed}, 失败={failed}, 跳过={skipped}")
    if failed_tests:
        print(f"失败的测试: {', '.join(failed_tests)}")
    
    return failed == 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="期货数据集合完整测试套件")
    parser.add_argument("--basic", action="store_true", help="只运行基础测试")
    parser.add_argument("--akshare", action="store_true", help="运行AKShare接口测试")
    parser.add_argument("--web", action="store_true", help="运行网站API更新功能测试（批量）")
    parser.add_argument("--playwright", action="store_true", help="运行Playwright自动化测试（逐个接口）")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    args = parser.parse_args()
    
    # 如果没有指定任何参数，默认运行基础测试
    if not any([args.basic, args.akshare, args.web, args.playwright, args.all]):
        args.basic = True
    
    results = {}
    
    print("="*70)
    print("期货数据集合完整测试套件")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # 1. 基础测试
    if args.basic or args.all:
        print("\n" + "="*70)
        print("[阶段1] 基础测试（文件存在性检查）")
        print("="*70)
        results["基础测试"] = run_basic_tests(include_akshare=False)
    
    # 2. AKShare接口测试
    if args.akshare or args.all:
        print("\n" + "="*70)
        print("[阶段2] AKShare接口测试")
        print("="*70)
        results["AKShare接口测试"] = run_basic_tests(include_akshare=True)
    
    # 3. 网站API更新功能测试（批量）
    if args.web or args.all:
        print("\n" + "="*70)
        print("[阶段3] 网站API更新功能测试（批量）")
        print("="*70)
        results["网站API测试"] = run_web_api_tests()
    
    # 4. Playwright自动化测试（逐个接口）
    if args.playwright or args.all:
        print("\n" + "="*70)
        print("[阶段4] Playwright自动化测试（逐个接口）")
        print("="*70)
        results["Playwright测试"] = run_playwright_tests()
    
    # 汇总结果
    print("\n" + "="*70)
    print("完整测试结果汇总")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*70)
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if all_passed:
        print("\n[SUCCESS] 所有测试通过！")
    else:
        print("\n[FAILED] 部分测试失败")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
