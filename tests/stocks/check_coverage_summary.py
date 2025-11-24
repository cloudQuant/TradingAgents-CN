"""
快速查看需求文档覆盖率摘要

使用方式:
    python check_coverage_summary.py
"""
import os
import re
import sys
from typing import Dict

# 添加项目根目录到路径
here = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(here, '..', '..')))


def extract_expected_collections(requirements_dir: str) -> Dict[str, str]:
    """从需求文档中提取集合名"""
    pattern = re.compile(r"http://localhost:3000/stocks/collections/([a-zA-Z0-9_\-]+)")
    mapping: Dict[str, str] = {}
    
    for root, _, files in os.walk(requirements_dir):
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    text = f.read()
                for name in pattern.findall(text):
                    mapping.setdefault(name, fp)
            except Exception:
                continue
    
    return mapping


def get_api_collections():
    """从后端API获取已实现的集合"""
    try:
        import httpx
        
        api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        url = f"{api_base_url}/api/stocks/collections"
        
        print(f"正在获取集合列表，请稍候（可能需要10-30秒）...")
        
        with httpx.Client(trust_env=False, timeout=60.0, follow_redirects=True) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                return {item.get("name") for item in data if isinstance(item, dict)}
    except httpx.TimeoutException as e:
        print(f"⚠ 后端API响应超时（超过60秒）: {e}")
    except Exception as e:
        print(f"⚠ 无法访问后端API: {e}")
    
    return set()


def main():
    # 获取需求文档目录
    req_dir = os.path.abspath(os.path.join(here, "requirements"))
    
    if not os.path.isdir(req_dir):
        print(f"❌ 需求文档目录不存在: {req_dir}")
        return
    
    print("正在扫描需求文档...")
    expected_map = extract_expected_collections(req_dir)
    
    print("正在查询后端 API...")
    actual_names = get_api_collections()
    
    # 统计
    total_expected = len(expected_map)
    total_actual = len(actual_names)
    existing = [name for name in expected_map.keys() if name in actual_names]
    missing = [name for name in expected_map.keys() if name not in actual_names]
    
    # 显示摘要
    print()
    print("="*80)
    print("📊 股票数据集合覆盖率摘要")
    print("="*80)
    print()
    print(f"📁 需求文档目录: {req_dir}")
    print(f"📄 需求文档中声明的集合: {total_expected} 个")
    print(f"🔌 后端API返回的集合:    {total_actual} 个")
    print()
    print("-"*80)
    print(f"✅ 已实现的集合: {len(existing)} 个")
    print(f"❌ 缺失的集合:   {len(missing)} 个")
    
    if total_expected > 0:
        coverage = 100 * len(existing) // total_expected
        print(f"📈 覆盖率: {coverage}% ({len(existing)}/{total_expected})")
    
    print("="*80)
    
    # 显示前10个缺失的集合
    if missing:
        print()
        print(f"❌ 缺失的集合（前10个）:")
        for idx, name in enumerate(sorted(missing)[:10], 1):
            doc = os.path.basename(expected_map[name])
            print(f"  {idx:2d}. {name}")
            print(f"      文档: {doc}")
        
        if len(missing) > 10:
            print(f"  ... 还有 {len(missing)-10} 个缺失的集合")
    
    # 显示前10个已实现的集合
    if existing:
        print()
        print(f"✅ 已实现的集合（前10个）:")
        for idx, name in enumerate(sorted(existing)[:10], 1):
            print(f"  {idx:2d}. {name}")
        
        if len(existing) > 10:
            print(f"  ... 还有 {len(existing)-10} 个已实现的集合")
    
    print()
    print("="*80)
    print("💡 提示:")
    print("  - 运行完整测试: pytest .\\collections\\test_collections_requirements_coverage.py -v -s")
    print("  - 查看详细报告: python view_latest_report.py")
    print("="*80)


if __name__ == "__main__":
    main()
