"""
验证后端集成是否成功
"""
import requests
import sys

API_URL = "http://localhost:8848/api/stocks/collections"

print("="*80)
print("验证后端集成")
print("="*80)

try:
    print(f"\n正在访问: {API_URL}")
    response = requests.get(API_URL, timeout=10)
    
    if response.status_code == 200:
        collections = response.json()
        total = len(collections)
        
        print(f"\n[SUCCESS] API响应成功!")
        print(f"集合总数: {total}")
        print(f"预期: 365 (75个已有 + 290个新增)")
        
        if total >= 365:
            print("\n✓ 集成成功! 所有集合都已加载")
            
            # 显示前10个新增的集合
            print("\n新增集合示例 (前10个):")
            new_collections = [c for c in collections if c.get('name', '').startswith(('news_', 'stock_a_', 'stock_account'))][:10]
            for idx, col in enumerate(new_collections, 1):
                print(f"  {idx}. {col.get('name')} - {col.get('display_name')}")
        else:
            print(f"\n[WARNING] 集合数量不足")
            print(f"当前: {total}, 预期: 365")
            print("可能原因:")
            print("  1. 后端服务还在加载中，请稍等几秒后重试")
            print("  2. 代码整合有问题，请检查 app/routers/stocks.py")
            sys.exit(1)
            
    elif response.status_code == 401:
        print("\n[WARNING] 需要认证")
        print("请先登录获取token，或检查是否需要鉴权")
    else:
        print(f"\n[ERROR] API返回错误状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        sys.exit(1)
        
except requests.exceptions.ConnectionError:
    print("\n[ERROR] 无法连接到后端服务")
    print("请确保后端服务正在运行:")
    print("  cd F:\\source_code\\TradingAgents-CN")
    print("  uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] 发生错误: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("验证完成!")
print("="*80)
print("\n后续步骤:")
print("1. 访问前端页面: http://localhost:3000/stocks/collections")
print("2. 检查是否显示365个集合")
print("3. 随机测试几个新集合的功能")
print("="*80)
