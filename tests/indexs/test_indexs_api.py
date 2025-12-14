"""
测试指数模块 API
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def get_token():
    """获取登录token"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("data", {}).get("access_token")
    return None

def test_collections_list(token):
    """测试获取集合列表"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/indexs/collections", headers=headers)
    
    print("\n=== 测试获取指数集合列表 ===")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            collections = data.get("data", [])
            print(f"✅ 成功获取 {len(collections)} 个集合")
            for c in collections:
                print(f"  - {c.get('name')}: {c.get('display_name')}")
            return True
        else:
            print(f"❌ 失败: {data.get('error')}")
    else:
        print(f"❌ HTTP错误: {response.status_code}")
    return False

def test_collection_stats(token, collection_name):
    """测试获取集合统计"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/indexs/collections/{collection_name}/stats", headers=headers)
    
    print(f"\n=== 测试获取集合统计: {collection_name} ===")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            stats = data.get("data", {})
            print(f"✅ 成功获取统计信息")
            print(f"  - 总数: {stats.get('total_count', 0)}")
            return True
        else:
            print(f"❌ 失败: {data.get('error')}")
    else:
        print(f"❌ HTTP错误: {response.status_code}")
    return False

def test_collection_data(token, collection_name):
    """测试获取集合数据"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/indexs/collections/{collection_name}?page=1&page_size=10", headers=headers)
    
    print(f"\n=== 测试获取集合数据: {collection_name} ===")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            result = data.get("data", {})
            items = result.get("items", [])
            total = result.get("total", 0)
            print(f"✅ 成功获取数据")
            print(f"  - 总数: {total}")
            print(f"  - 当前页: {len(items)} 条")
            return True
        else:
            print(f"❌ 失败: {data.get('error')}")
    else:
        print(f"❌ HTTP错误: {response.status_code}")
    return False

def test_update_config(token, collection_name):
    """测试获取更新配置"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/indexs/collections/{collection_name}/update-config", headers=headers)
    
    print(f"\n=== 测试获取更新配置: {collection_name} ===")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            config = data.get("data", {})
            print(f"✅ 成功获取更新配置")
            print(f"  - 显示名称: {config.get('display_name')}")
            print(f"  - 单条更新: {'启用' if config.get('single_update', {}).get('enabled') else '禁用'}")
            print(f"  - 批量更新: {'启用' if config.get('batch_update', {}).get('enabled') else '禁用'}")
            return True
        else:
            print(f"❌ 失败: {data.get('error')}")
    else:
        print(f"❌ HTTP错误: {response.status_code}")
    return False

def main():
    print("=" * 60)
    print("指数模块 API 测试")
    print("=" * 60)
    
    # 获取token
    print("\n正在登录...")
    token = get_token()
    if not token:
        print("❌ 登录失败，无法继续测试")
        sys.exit(1)
    print("✅ 登录成功")
    
    # 测试集合列表
    if not test_collections_list(token):
        print("\n❌ 集合列表测试失败")
        sys.exit(1)
    
    # 测试各个集合的API
    collections_to_test = [
        "stock_zh_index_spot_sina",
        "stock_zh_index_spot_em",
        "stock_hk_index_spot_sina",
        "stock_hk_index_spot_em",
        "index_global_spot_em",
    ]
    
    success_count = 0
    for collection_name in collections_to_test:
        if test_collection_stats(token, collection_name):
            success_count += 1
        if test_collection_data(token, collection_name):
            success_count += 1
        if test_update_config(token, collection_name):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {success_count}/{len(collections_to_test) * 3} 成功")
    print("=" * 60)

if __name__ == "__main__":
    main()
