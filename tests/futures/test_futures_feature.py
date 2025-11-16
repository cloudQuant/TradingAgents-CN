"""
期货投研功能测试
验证期货投研相关的页面和功能是否正确实现
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestFuturesFeature:
    """测试期货投研功能"""

    def test_sidebar_menu_has_futures_button(self):
        """测试侧边栏是否有期货投研按钮"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        assert os.path.exists(sidebar_path), f"侧边栏文件不存在: {sidebar_path}"
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有期货投研的 el-sub-menu
        assert 'index="/futures"' in content, "侧边栏中找不到期货投研菜单 (index=\"/futures\")"
        assert '期货投研' in content or '期货分析' in content, "侧边栏中找不到'期货投研'或'期货分析'文本"
        
        print("[OK] 侧边栏包含期货投研菜单")

    def test_sidebar_menu_has_overview_option(self):
        """测试期货投研下是否有概览选项"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找期货投研菜单块
        futures_start = content.find('index="/futures"')
        assert futures_start > 0, "找不到期货投研菜单"
        
        # 在期货投研菜单块中查找概览
        futures_end = content.find('</el-sub-menu>', futures_start)
        futures_block = content[futures_start:futures_end]
        
        assert 'index="/futures/overview"' in futures_block, "期货投研菜单中找不到概览选项"
        assert '概览' in futures_block, "期货投研菜单中找不到'概览'文本"
        
        print("[OK] 期货投研菜单包含概览选项")

    def test_sidebar_menu_has_collections_option(self):
        """测试期货投研下是否有数据集合选项"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找期货投研菜单块
        futures_start = content.find('index="/futures"')
        assert futures_start > 0, "找不到期货投研菜单"
        
        futures_end = content.find('</el-sub-menu>', futures_start)
        futures_block = content[futures_start:futures_end]
        
        assert 'index="/futures/collections"' in futures_block, "期货投研菜单中找不到数据集合选项"
        assert '数据集合' in futures_block, "期货投研菜单中找不到'数据集合'文本"
        
        print("[OK] 期货投研菜单包含数据集合选项")

    def test_sidebar_menu_has_analysis_option(self):
        """测试期货投研下是否有期货分析选项"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找期货投研菜单块
        futures_start = content.find('index="/futures"')
        assert futures_start > 0, "找不到期货投研菜单"
        
        futures_end = content.find('</el-sub-menu>', futures_start)
        futures_block = content[futures_start:futures_end]
        
        assert 'index="/futures/analysis"' in futures_block, "期货投研菜单中找不到期货分析选项"
        assert '期货分析' in futures_block, "期货投研菜单中找不到'期货分析'文本"
        
        print("[OK] 期货投研菜单包含期货分析选项")

    def test_router_has_futures_routes(self):
        """测试路由配置是否包含期货投研路由"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'router', 'index.ts'
        )
        router_path = os.path.abspath(router_path)
        
        assert os.path.exists(router_path), f"路由文件不存在: {router_path}"
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有 /futures 路由
        assert "path: '/futures'" in content, "路由配置中找不到 /futures 路径"
        
        # 验证有 overview 子路由
        assert "path: 'overview'" in content or "'overview'" in content, "路由配置中找不到 overview 子路由"
        
        # 验证有 collections 子路由  
        assert "path: 'collections'" in content or "'collections'" in content, "路由配置中找不到 collections 子路由"
        
        # 验证有 analysis 子路由
        assert "path: 'analysis'" in content or "'analysis'" in content, "路由配置中找不到 analysis 子路由"
        
        print("[OK] 路由配置包含期货投研相关路由")

    def test_futures_overview_page_exists(self):
        """测试期货概览页面文件是否存在"""
        overview_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Futures', 'index.vue'
        )
        overview_path = os.path.abspath(overview_path)
        
        assert os.path.exists(overview_path), f"期货概览页面文件不存在: {overview_path}"
        
        print("[OK] 期货概览页面文件存在")

    def test_futures_collections_page_exists(self):
        """测试期货数据集合页面文件是否存在"""
        collections_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Futures', 'Collections.vue'
        )
        collections_path = os.path.abspath(collections_path)
        
        assert os.path.exists(collections_path), f"期货数据集合页面文件不存在: {collections_path}"
        
        print("[OK] 期货数据集合页面文件存在")

    def test_futures_analysis_page_exists(self):
        """测试期货分析页面文件是否存在"""
        analysis_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Futures', 'FuturesAnalysis.vue'
        )
        analysis_path = os.path.abspath(analysis_path)
        
        assert os.path.exists(analysis_path), f"期货分析页面文件不存在: {analysis_path}"
        
        print("[OK] 期货分析页面文件存在")

    def test_backend_futures_router_exists(self):
        """测试后端期货路由文件是否存在"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'app', 'routers', 'futures.py'
        )
        router_path = os.path.abspath(router_path)
        
        assert os.path.exists(router_path), f"后端期货路由文件不存在: {router_path}"
        
        # 验证路由文件中有基本的API端点定义
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'APIRouter' in content, "路由文件中找不到 APIRouter"
        assert 'router = APIRouter' in content, "路由文件中找不到 router 定义"
        assert '/api/futures' in content, "路由文件中找不到 /api/futures 前缀"
        
        print("[OK] 后端期货路由文件存在且配置正确")


if __name__ == "__main__":
    # 直接运行所有测试
    import sys
    test = TestFuturesFeature()
    failed = 0
    
    print("="*70)
    print("期货投研功能测试")
    print("="*70)
    
    tests = [
        ('test_sidebar_menu_has_futures_button', '侧边栏期货投研菜单'),
        ('test_sidebar_menu_has_overview_option', '概览选项'),
        ('test_sidebar_menu_has_collections_option', '数据集合选项'),
        ('test_sidebar_menu_has_analysis_option', '期货分析选项'),
        ('test_router_has_futures_routes', '路由配置'),
        ('test_futures_overview_page_exists', '概览页面文件'),
        ('test_futures_collections_page_exists', '数据集合页面文件'),
        ('test_futures_analysis_page_exists', '期货分析页面文件'),
        ('test_backend_futures_router_exists', '后端路由文件'),
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
