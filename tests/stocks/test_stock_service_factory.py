"""
股票数据服务工厂测试脚本
验证重构后的服务工厂能够正确加载所有服务
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_service_factory():
    """测试服务工厂"""
    print("=" * 60)
    print("股票数据服务工厂测试")
    print("=" * 60)
    
    try:
        from app.services.data_sources.stocks.service_factory import (
            StockServiceFactory,
            get_supported_stock_collections
        )
        
        # 获取支持的集合列表
        collections = get_supported_stock_collections()
        print(f"\n[+] 成功加载服务工厂")
        print(f"[+] 支持的数据集合数量: {len(collections)}")
        
        # 显示部分集合名称
        print(f"\n前 20 个集合:")
        for i, name in enumerate(collections[:20]):
            print(f"  {i+1}. {name}")
        
        if len(collections) > 20:
            print(f"  ... 还有 {len(collections) - 20} 个集合")
        
        # 按类别统计
        categories = {
            "实时行情 (spot)": [c for c in collections if "spot" in c],
            "历史数据 (hist)": [c for c in collections if "hist" in c],
            "涨停股池 (zt_pool)": [c for c in collections if "zt_pool" in c],
            "龙虎榜 (lhb)": [c for c in collections if "lhb" in c],
            "港股 (hk)": [c for c in collections if "_hk_" in c],
            "美股 (us)": [c for c in collections if "_us_" in c],
            "板块 (board)": [c for c in collections if "board" in c],
            "ESG": [c for c in collections if "esg" in c],
            "财务 (financial)": [c for c in collections if "financial" in c],
        }
        
        print(f"\n按类别统计:")
        for category, items in categories.items():
            print(f"  {category}: {len(items)} 个")
        
        return True
        
    except Exception as e:
        print(f"\n[x] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """测试更新配置"""
    print("\n" + "=" * 60)
    print("股票数据更新配置测试")
    print("=" * 60)
    
    try:
        from app.config.stock_update_config import (
            get_collection_update_config,
            get_all_collection_update_configs,
            COLLECTION_TYPES
        )
        
        # 获取所有配置
        configs = get_all_collection_update_configs()
        print(f"\n[+] 配置中定义的集合数量: {len(configs)}")
        
        # 显示配置类型统计
        print(f"\n配置类型统计:")
        for ctype, collections in COLLECTION_TYPES.items():
            print(f"  {ctype}: {len(collections)} 个")
        
        # 测试获取单个配置
        test_collection = "stock_zh_a_spot_em"
        config = get_collection_update_config(test_collection)
        print(f"\n测试配置 ({test_collection}):")
        print(f"  display_name: {config.get('display_name')}")
        print(f"  akshare_func: {config.get('akshare_func')}")
        print(f"  unique_keys: {config.get('unique_keys')}")
        print(f"  single_update enabled: {config.get('single_update', {}).get('enabled')}")
        print(f"  batch_update enabled: {config.get('batch_update', {}).get('enabled')}")
        
        return True
        
    except Exception as e:
        print(f"\n[x] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_refresh_service_v2():
    """测试 V2 刷新服务"""
    print("\n" + "=" * 60)
    print("股票刷新服务 V2 测试")
    print("=" * 60)
    
    try:
        from app.services.stock_refresh_service_v2 import StockRefreshService
        
        # 创建服务实例（不连接数据库）
        print("\n[+] 尝试导入 StockRefreshService V2...")
        print("[+] 导入成功!")
        
        # 检查支持的集合
        # 注意：这需要数据库连接，所以这里只测试类的存在性
        print("[+] StockRefreshService V2 类可用")
        
        return True
        
    except Exception as e:
        print(f"\n[x] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    results = []
    
    results.append(("服务工厂", test_service_factory()))
    results.append(("更新配置", test_config()))
    results.append(("刷新服务V2", test_refresh_service_v2()))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过!")
    else:
        print("部分测试失败，请检查上面的错误信息")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
