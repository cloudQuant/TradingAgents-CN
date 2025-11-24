"""
快速检查当前状态

显示：
1. 需求文档中声明了多少个集合
2. API 实际返回了多少个集合
3. 缺少了多少个集合
"""
import os
import re
import sys

def extract_collections_from_requirements():
    """从需求文档提取集合名"""
    here = os.path.dirname(__file__)
    req_dir = os.path.abspath(os.path.join(here, "requirements"))
    
    pattern = re.compile(r"http://localhost:3000/stocks/collections/([a-zA-Z0-9_\-]+)")
    collections = set()
    
    for root, _, files in os.walk(req_dir):
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    text = f.read()
                for name in pattern.findall(text):
                    collections.add(name)
            except Exception:
                continue
    
    return collections


def get_api_collections():
    """从后端API获取集合列表"""
    try:
        import httpx
        api_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        url = f"{api_url}/api/stocks/collections"
        
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
    print("="*80)
    print("🔍 股票数据集合快速检查")
    print("="*80)
    print()
    
    print("正在扫描需求文档...")
    required = extract_collections_from_requirements()
    
    print("正在查询后端API...")
    implemented = get_api_collections()
    
    missing = required - implemented
    extra = implemented - required
    
    print()
    print("="*80)
    print("📊 统计结果")
    print("="*80)
    print(f"📄 需求文档中声明: {len(required):3d} 个集合")
    print(f"✅ 后端API已实现:  {len(implemented):3d} 个集合")
    print(f"❌ 缺少实现:       {len(missing):3d} 个集合")
    if extra:
        print(f"⚠️  API额外集合:     {len(extra):3d} 个（未在需求文档中）")
    
    if len(required) > 0:
        coverage = 100 * len(implemented & required) / len(required)
        print(f"📈 覆盖率:         {coverage:.1f}%")
    
    print("="*80)
    
    if missing:
        print()
        print(f"❌ 缺少的集合（前20个）：")
        for idx, name in enumerate(sorted(missing)[:20], 1):
            print(f"   {idx:2d}. {name}")
        if len(missing) > 20:
            print(f"   ... 还有 {len(missing)-20} 个")
    
    if extra:
        print()
        print(f"⚠️ API中额外的集合（未在需求文档中）：")
        for idx, name in enumerate(sorted(extra), 1):
            print(f"   {idx:2d}. {name}")
    
    print()
    print("="*80)
    print("💡 提示:")
    print("   这个快速检查可以帮你了解：")
    print("   - 需求文档中定义了多少个集合（应该是365个左右）")
    print("   - 后端API当前实现了多少个集合")
    print("   - 还有多少个集合需要实现")
    print("   注意：后端API可能需要10-30秒响应时间")
    print("="*80)


if __name__ == "__main__":
    main()
