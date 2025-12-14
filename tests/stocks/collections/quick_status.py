"""
快速检查股票数据集合的实现状态

显示：
1. 需求文档中声明的集合数量
2. 已有测试文件的集合数量
3. 覆盖率统计
"""
import os
import re
from typing import Dict, Set


def extract_collections_from_docs(req_dir: str) -> Dict[str, str]:
    """从需求文档中提取集合名称"""
    pattern = re.compile(r'http://localhost:3000/stocks/collections/([a-zA-Z0-9_\-]+)')
    collections = {}
    
    for fn in os.listdir(req_dir):
        if not fn.endswith('.md'):
            continue
        
        fp = os.path.join(req_dir, fn)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                text = f.read()
            for name in pattern.findall(text):
                if name not in collections:
                    collections[name] = fn
        except:
            continue
    
    return collections


def get_test_files(collections_dir: str) -> Set[str]:
    """获取已有测试文件对应的集合名称"""
    existing = set()
    for fn in os.listdir(collections_dir):
        if fn.endswith('_collection.py') and fn[0].isdigit():
            match = re.match(r'\d+_(.+)_collection\.py', fn)
            if match:
                existing.add(match.group(1))
    return existing


def main():
    """主函数"""
    # 获取目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_dir = os.path.join(script_dir, '..', 'requirements')
    
    print("=" * 60)
    print("股票数据集合实现状态检查")
    print("=" * 60)
    
    # 从需求文档提取集合
    collections_from_docs = extract_collections_from_docs(req_dir)
    print(f"\n需求文档中声明的集合: {len(collections_from_docs)} 个")
    
    # 获取已有测试文件
    test_collections = get_test_files(script_dir)
    print(f"已有测试文件的集合: {len(test_collections)} 个")
    
    # 计算覆盖率
    covered = set(collections_from_docs.keys()) & test_collections
    missing = set(collections_from_docs.keys()) - test_collections
    extra = test_collections - set(collections_from_docs.keys())
    
    print(f"\n覆盖情况:")
    print(f"  已覆盖: {len(covered)} 个")
    print(f"  缺失测试: {len(missing)} 个")
    print(f"  额外测试: {len(extra)} 个")
    
    coverage = 100 * len(covered) / len(collections_from_docs) if collections_from_docs else 0
    print(f"\n测试覆盖率: {coverage:.1f}%")
    
    if missing:
        print(f"\n缺失测试的集合 ({len(missing)} 个):")
        for name in sorted(missing)[:20]:
            doc = collections_from_docs.get(name, "未知")
            print(f"  - {name} <- {doc}")
        if len(missing) > 20:
            print(f"  ... 还有 {len(missing) - 20} 个")
    
    if extra:
        print(f"\n额外的测试文件 ({len(extra)} 个):")
        for name in sorted(extra)[:10]:
            print(f"  - {name}")
        if len(extra) > 10:
            print(f"  ... 还有 {len(extra) - 10} 个")
    
    print("\n" + "=" * 60)
    
    # 返回状态
    if len(missing) == 0:
        print("✓ 所有需求文档中的集合都有对应的测试文件！")
        return 0
    else:
        print(f"⚠ 还有 {len(missing)} 个集合需要创建测试文件")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
