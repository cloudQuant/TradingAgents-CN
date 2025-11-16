"""
数字货币投研功能测试
验证数字货币投研相关的页面和功能是否正确实现
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestCryptosFeature:
    """测试数字货币投研功能"""

    def test_sidebar_menu_has_cryptos_button(self):
        """测试侧边栏是否有数字货币投研按钮"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        assert os.path.exists(sidebar_path), f"侧边栏文件不存在: {sidebar_path}"
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'index="/cryptos"' in content, "侧边栏中找不到数字货币投研菜单"
        assert '数字货币投研' in content or '数字货币分析' in content, "侧边栏中找不到'数字货币投研'文本"
        print("[OK] 侧边栏包含数字货币投研菜单")

    def test_router_has_cryptos_routes(self):
        """测试路由配置是否包含数字货币投研路由"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'router', 'index.ts'
        )
        router_path = os.path.abspath(router_path)
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "path: '/cryptos'" in content, "路由配置中找不到 /cryptos 路径"
        print("[OK] 路由配置包含数字货币投研相关路由")

    def test_cryptos_pages_exist(self):
        """测试数字货币页面文件是否存在"""
        pages = [
            ('index.vue', '概览页面'),
            ('Collections.vue', '数据集合页面'),
            ('CryptosAnalysis.vue', '数字货币分析页面')
        ]
        
        for filename, desc in pages:
            page_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', 'frontend', 'src', 'views', 'Cryptos', filename
            )
            page_path = os.path.abspath(page_path)
            assert os.path.exists(page_path), f"数字货币{desc}文件不存在: {page_path}"
            print(f"[OK] 数字货币{desc}文件存在")

    def test_backend_cryptos_router_exists(self):
        """测试后端数字货币路由文件是否存在"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'app', 'routers', 'cryptos.py'
        )
        router_path = os.path.abspath(router_path)
        
        assert os.path.exists(router_path), f"后端数字货币路由文件不存在: {router_path}"
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'APIRouter' in content, "路由文件中找不到 APIRouter"
        assert '/api/cryptos' in content, "路由文件中找不到 /api/cryptos 前缀"
        print("[OK] 后端数字货币路由文件存在且配置正确")


if __name__ == "__main__":
    import sys
    test = TestCryptosFeature()
    failed = 0
    
    print("="*70)
    print("数字货币投研功能测试")
    print("="*70)
    
    tests = [
        ('test_sidebar_menu_has_cryptos_button', '侧边栏数字货币投研菜单'),
        ('test_router_has_cryptos_routes', '路由配置'),
        ('test_cryptos_pages_exist', '页面文件'),
        ('test_backend_cryptos_router_exists', '后端路由文件'),
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
