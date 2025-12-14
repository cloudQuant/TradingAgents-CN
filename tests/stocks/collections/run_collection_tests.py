"""
股票数据集合测试运行脚本

功能：
1. 运行所有集合测试
2. 生成测试报告
3. 统计测试覆盖率
"""
import os
import re
import sys
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple


def get_all_test_files(collections_dir: str) -> List[str]:
    """获取所有测试文件"""
    test_files = []
    for fn in os.listdir(collections_dir):
        if fn.endswith('_collection.py') and fn[0].isdigit():
            test_files.append(fn)
    return sorted(test_files)


def extract_collection_name(filename: str) -> str:
    """从文件名提取集合名称"""
    match = re.match(r'\d+_(.+)_collection\.py', filename)
    if match:
        return match.group(1)
    return None


def run_single_test(test_file: str, collections_dir: str) -> Tuple[bool, str]:
    """运行单个测试文件"""
    try:
        result = subprocess.run(
            ['python3', '-m', 'pytest', test_file, '-v', '--tb=short'],
            cwd=collections_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "测试超时"
    except Exception as e:
        return False, str(e)


def main():
    """主函数"""
    print("=" * 70)
    print("股票数据集合测试运行器")
    print("=" * 70)
    
    # 获取目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取所有测试文件
    test_files = get_all_test_files(script_dir)
    print(f"\n找到 {len(test_files)} 个测试文件")
    
    # 检查环境变量
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8848")
    auth_token = os.getenv("API_AUTH_TOKEN", "")
    
    print(f"\n环境配置:")
    print(f"  API_BASE_URL: {api_base_url}")
    print(f"  API_AUTH_TOKEN: {'已设置' if auth_token else '未设置'}")
    
    if not auth_token:
        print("\n警告: API_AUTH_TOKEN 未设置，大部分测试将被跳过")
        print("请设置环境变量后重新运行:")
        print("  export API_AUTH_TOKEN=your_token_here")
        print("  export API_BASE_URL=http://localhost:8848")
    
    # 统计
    total = len(test_files)
    passed = 0
    failed = 0
    skipped = 0
    
    results = []
    
    print(f"\n开始运行测试...")
    print("-" * 70)
    
    for idx, test_file in enumerate(test_files, 1):
        collection_name = extract_collection_name(test_file)
        print(f"[{idx:3d}/{total}] 测试 {collection_name}...", end=" ", flush=True)
        
        success, output = run_single_test(test_file, script_dir)
        
        # 分析结果
        if "skipped" in output.lower() and "passed" not in output.lower():
            status = "SKIP"
            skipped += 1
        elif success:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        results.append({
            'file': test_file,
            'collection': collection_name,
            'status': status,
            'output': output
        })
        
        status_icon = "✓" if status == "PASS" else ("⊘" if status == "SKIP" else "✗")
        print(f"{status_icon} {status}")
    
    # 输出统计
    print("\n" + "=" * 70)
    print("测试结果统计")
    print("=" * 70)
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  跳过: {skipped}")
    print(f"  总计: {total}")
    
    if passed + failed > 0:
        print(f"  通过率: {100 * passed / (passed + failed):.1f}%")
    
    # 输出失败的测试
    if failed > 0:
        print("\n" + "-" * 70)
        print("失败的测试:")
        for r in results:
            if r['status'] == 'FAIL':
                print(f"  - {r['collection']} ({r['file']})")
    
    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(script_dir, f"test_report_{timestamp}.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("股票数据集合测试报告\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"通过: {passed}\n")
        f.write(f"失败: {failed}\n")
        f.write(f"跳过: {skipped}\n")
        f.write(f"总计: {total}\n\n")
        
        f.write("详细结果:\n")
        f.write("-" * 70 + "\n")
        for r in results:
            f.write(f"\n{r['status']:4s} | {r['collection']}\n")
            if r['status'] == 'FAIL':
                f.write(f"输出:\n{r['output']}\n")
    
    print(f"\n报告已保存到: {report_file}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
