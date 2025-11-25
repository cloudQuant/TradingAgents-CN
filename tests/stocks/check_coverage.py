"""
检查股票集合覆盖率
对比 routers/stocks.py 中定义的集合和实际存在的服务
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def get_router_collections():
    """从 routers/stocks.py 中提取集合名称"""
    router_file = 'F:/source_code/TradingAgents-CN/app/routers/stocks.py'
    with open(router_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 "name": "xxx" 模式
    collections = re.findall(r'"name":\s*"([^"]+)"', content)
    # 过滤出股票相关的集合
    stock_collections = [c for c in collections if c.startswith('stock_') or c.startswith('news_')]
    return list(set(stock_collections))

def get_service_collections():
    """获取已实现的服务集合"""
    from app.services.data_sources.stocks.service_factory import get_supported_stock_collections
    return get_supported_stock_collections()

def main():
    print("=" * 60)
    print("股票数据集合覆盖率检查")
    print("=" * 60)
    
    router_collections = set(get_router_collections())
    service_collections = set(get_service_collections())
    
    print(f"\n路由中定义的集合数量: {len(router_collections)}")
    print(f"已实现服务的集合数量: {len(service_collections)}")
    
    # 找出缺失的服务
    missing_services = router_collections - service_collections
    # 找出多余的服务
    extra_services = service_collections - router_collections
    
    print(f"\n缺失服务的集合数量: {len(missing_services)}")
    if missing_services:
        print("缺失的集合 (前20个):")
        for i, c in enumerate(sorted(missing_services)[:20]):
            print(f"  {i+1}. {c}")
        if len(missing_services) > 20:
            print(f"  ... 还有 {len(missing_services) - 20} 个")
    
    print(f"\n多余服务的集合数量: {len(extra_services)}")
    if extra_services:
        print("多余的集合 (前10个):")
        for i, c in enumerate(sorted(extra_services)[:10]):
            print(f"  {i+1}. {c}")
    
    # 计算覆盖率
    if router_collections:
        coverage = len(router_collections & service_collections) / len(router_collections) * 100
        print(f"\n覆盖率: {coverage:.1f}%")
    
    return len(missing_services) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
