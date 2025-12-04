"""
运行所有债券数据集合测试
"""
import os
import sys
import importlib.util

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


def run_all_tests():
    """运行所有测试"""
    tests_dir = os.path.dirname(__file__)
    
    # 获取所有测试文件
    test_files = sorted([
        f for f in os.listdir(tests_dir)
        if f.startswith('test_') and f.endswith('.py') and f != 'test_base.py'
    ])
    
    print("="*70)
    print("债券数据集合测试套件")
    print(f"共 {len(test_files)} 个测试文件")
    print("="*70)
    
    results = []
    
    for test_file in test_files:
        # 提取集合名称
        # test_01_bond_info_cm.py -> bond_info_cm
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
                success = test_instance.run_all_tests()
                results.append((collection_name, success))
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
    
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"跳过: {skipped}")
    print(f"总计: {len(results)}")
    
    if failed > 0:
        print("\n失败的测试:")
        for name, result in results:
            if result is False:
                print(f"  - {name}")
    
    print("="*70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
