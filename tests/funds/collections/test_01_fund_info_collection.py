"""
基金基本信息数据集合测试用例
测试基金基本信息集合的刷新、更新数据、清空数据等功能
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class TestFundInfoCollection:
    """测试基金基本信息数据集合"""

    def test_fund_collections_list_includes_fund_name_em(self):
        """测试基金集合列表中包含fund_name_em（基金基本信息）"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 'app', 'routers', 'funds.py'
        )
        router_path = os.path.abspath(router_path)
        
        assert os.path.exists(router_path), f"基金路由文件不存在: {router_path}"
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有fund_name_em集合
        assert 'fund_name_em' in content, "路由中找不到fund_name_em集合定义"
        print("[OK] 基金路由包含fund_name_em集合")

    def test_fund_refresh_endpoint_exists(self):
        """测试基金集合刷新端点存在"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 'app', 'routers', 'funds.py'
        )
        router_path = os.path.abspath(router_path)
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有刷新端点
        assert 'refresh' in content.lower(), "路由中找不到refresh相关端点"
        print("[OK] 基金路由包含refresh端点")

    def test_fund_clear_endpoint_exists(self):
        """测试基金集合清空端点存在"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 'app', 'routers', 'funds.py'
        )
        router_path = os.path.abspath(router_path)
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有清空端点
        assert 'clear' in content.lower(), "路由中找不到clear相关端点"
        print("[OK] 基金路由包含clear端点")

    def test_fund_data_service_exists(self):
        """测试基金数据服务文件存在"""
        service_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 'app', 'services', 'fund_data_service.py'
        )
        service_path = os.path.abspath(service_path)
        
        assert os.path.exists(service_path), f"基金数据服务文件不存在: {service_path}"
        
        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有fund_name_em相关实现
        assert 'fund_name_em' in content, "数据服务中找不到fund_name_em相关实现"
        print("[OK] 基金数据服务包含fund_name_em实现")

    def test_fund_refresh_service_exists(self):
        """测试基金刷新服务存在"""
        service_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 'app', 'services', 'fund_refresh_service.py'
        )
        service_path = os.path.abspath(service_path)
        
        assert os.path.exists(service_path), f"基金刷新服务文件不存在: {service_path}"
        
        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有fund_name_em刷新实现
        assert 'fund_name_em' in content, "刷新服务中找不到fund_name_em相关实现"
        print("[OK] 基金刷新服务包含fund_name_em实现")

    def test_frontend_fund_collection_page_exists(self):
        """测试前端基金集合详情页存在"""
        page_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 'frontend', 'src', 'views', 'Funds', 'Collection.vue'
        )
        page_path = os.path.abspath(page_path)
        
        assert os.path.exists(page_path), f"前端基金集合详情页不存在: {page_path}"
        
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有刷新、清空等功能
        assert '更新数据' in content or 'refresh' in content.lower(), "页面中找不到更新数据功能"
        assert '清空' in content or 'clear' in content.lower(), "页面中找不到清空数据功能"
        print("[OK] 前端基金集合详情页包含必要功能")


if __name__ == "__main__":
    import sys
    test = TestFundInfoCollection()
    failed = 0
    
    print("="*70)
    print("基金基本信息数据集合测试")
    print("="*70)
    
    tests = [
        ('test_fund_collections_list_includes_fund_name_em', '集合列表包含fund_name_em'),
        ('test_fund_refresh_endpoint_exists', '刷新端点存在'),
        ('test_fund_clear_endpoint_exists', '清空端点存在'),
        ('test_fund_data_service_exists', '数据服务存在'),
        ('test_fund_refresh_service_exists', '刷新服务存在'),
        ('test_frontend_fund_collection_page_exists', '前端集合详情页存在'),
    ]
    
    for test_method, test_name in tests:
        try:
            print(f"\n[测试] {test_name}...")
            getattr(test, test_method)()
            print(f"  [OK] 通过")
        except AssertionError as e:
            print(f"  [FAILED] 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] 错误: {e}")
            failed += 1
    
    print("\n" + "="*70)
    if failed == 0:
        print("[SUCCESS] 所有测试通过！")
        print("="*70)
        sys.exit(0)
    else:
        print(f"[FAILED] {failed} 个测试失败")
        print("="*70)
        sys.exit(1)
