"""
查看最新的测试覆盖率报告

使用方式:
    python view_latest_report.py
"""
import os
import glob
from datetime import datetime


def find_latest_report():
    """查找最新的测试报告文件"""
    here = os.path.dirname(__file__)
    pattern = os.path.join(here, "test_coverage_report_*.log")
    
    log_files = glob.glob(pattern)
    if not log_files:
        print("未找到任何测试报告文件")
        print(f"搜索路径: {pattern}")
        return None
    
    # 按修改时间排序，获取最新的
    latest = max(log_files, key=os.path.getmtime)
    return latest


def display_report(log_file):
    """显示报告内容"""
    if not os.path.exists(log_file):
        print(f"报告文件不存在: {log_file}")
        return
    
    # 获取文件信息
    file_size = os.path.getsize(log_file)
    mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
    
    print("="*80)
    print("最新测试报告")
    print("="*80)
    print(f"文件路径: {log_file}")
    print(f"文件大小: {file_size} 字节")
    print(f"生成时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print()
    
    # 读取并显示内容
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(content)
    
    print()
    print("="*80)
    print(f"报告文件: {log_file}")
    print("="*80)


def main():
    latest = find_latest_report()
    if latest:
        display_report(latest)
    else:
        print("\n请先运行测试生成报告:")
        print("pytest .\\collections\\test_collections_requirements_coverage.py -v -s")


if __name__ == "__main__":
    main()
