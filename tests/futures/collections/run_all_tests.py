"""
运行所有期货数据集合测试
支持多种测试模式：文件检查、AKShare接口测试、API功能测试
"""
import os
import sys
import argparse
import importlib.util

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


def run_all_tests(include_api_tests: bool = False, include_akshare_tests: bool = False):
    """运行所有测试
    
    Args:
        include_api_tests: 是否包含API功能测试（需要服务器运行）
        include_akshare_tests: 是否包含AKShare接口测试
    """
    tests_dir = os.path.dirname(__file__)
    
    # 获取所有测试文件
    test_files = sorted([
        f for f in os.listdir(tests_dir)
        if f.startswith('test_') and f.endswith('.py') 
        and f != 'test_base.py' 
        and f != 'test_api_update.py'
    ])
    
    print("="*70)
    print("期货数据集合测试套件")
    print(f"共 {len(test_files)} 个测试文件")
    if include_api_tests:
        print("模式: 包含API功能测试")
    if include_akshare_tests:
        print("模式: 包含AKShare接口测试")
    print("="*70)
    
    results = []
    akshare_results = []
    
    for test_file in test_files:
        # 提取集合名称
        # test_01_futures_fees_info.py -> futures_fees_info
        parts = test_file.replace('.py', '').split('_')
        collection_name = '_'.join(parts[2:])
        
        print(f"\n[{test_file}] 测试 {collection_name}...")
        
        # 动态导入测试模块
        spec = importlib.util.spec_from_file_location(
            f"test_{collection_name}",
            os.path.join(tests_dir, test_file)
        )
        module = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(module)
            
            # 找到测试类
            test_class = None
            for name in dir(module):
                if name.startswith('Test') and name.endswith('Collection'):
                    test_class = getattr(module, name)
                    break
            
            if test_class:
                test_instance = test_class()
                
                # 运行基础测试
                success = test_instance.run_all_tests(include_api_tests=include_api_tests)
                results.append((collection_name, success))
                
                # 运行AKShare接口测试
                if include_akshare_tests and hasattr(test_instance, 'test_akshare_interface'):
                    try:
                        test_instance.test_akshare_interface()
                        akshare_results.append((collection_name, True))
                    except Exception as e:
                        print(f"  [WARN] AKShare测试失败: {e}")
                        akshare_results.append((collection_name, False))
            else:
                print(f"  [WARN] 未找到测试类")
                results.append((collection_name, None))
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append((collection_name, False))
    
    # 输出汇总
    print("\n" + "="*70)
    print("测试结果汇总")
    print("="*70)
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    
    print(f"\n基础测试:")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  跳过: {skipped}")
    print(f"  总计: {len(results)}")
    
    if include_akshare_tests and akshare_results:
        ak_passed = sum(1 for _, r in akshare_results if r is True)
        ak_failed = sum(1 for _, r in akshare_results if r is False)
        print(f"\nAKShare接口测试:")
        print(f"  通过: {ak_passed}")
        print(f"  失败: {ak_failed}")
        print(f"  总计: {len(akshare_results)}")
    
    if failed > 0:
        print("\n失败的基础测试:")
        for name, result in results:
            if result is False:
                print(f"  - {name}")
    
    if include_akshare_tests:
        ak_failed_list = [name for name, r in akshare_results if r is False]
        if ak_failed_list:
            print("\n失败的AKShare测试:")
            for name in ak_failed_list:
                print(f"  - {name}")
    
    print("="*70)
    
    return failed == 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="期货数据集合测试套件")
    parser.add_argument("--api", action="store_true", help="包含API功能测试（需要服务器运行）")
    parser.add_argument("--akshare", action="store_true", help="包含AKShare接口测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    args = parser.parse_args()
    
    include_api = args.api or args.all
    include_akshare = args.akshare or args.all
    
    success = run_all_tests(
        include_api_tests=include_api,
        include_akshare_tests=include_akshare
    )
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
