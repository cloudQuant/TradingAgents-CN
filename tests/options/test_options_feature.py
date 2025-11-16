"""
期权投研功能测试
验证期权投研相关的页面和功能是否正确实现
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestOptionsFeature:
    """测试期权投研功能"""

    def test_sidebar_menu_has_options_button(self):
        """测试侧边栏是否有期权投研按钮"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        assert os.path.exists(sidebar_path), f"侧边栏文件不存在: {sidebar_path}"
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有期权投研的 el-sub-menu
        assert 'index="/options"' in content, "侧边栏中找不到期权投研菜单 (index=\"/options\")"
        assert '期权投研' in content or '期权分析' in content, "侧边栏中找不到'期权投研'或'期权分析'文本"
        
        print("[OK] 侧边栏包含期权投研菜单")

    def test_sidebar_menu_has_overview_option(self):
        """测试期权投研下是否有概览选项"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找期权投研菜单块
        options_start = content.find('index="/options"')
        assert options_start > 0, "找不到期权投研菜单"
        
        # 在期权投研菜单块中查找概览
        options_end = content.find('</el-sub-menu>', options_start)
        options_block = content[options_start:options_end]
        
        assert 'index="/options/overview"' in options_block, "期权投研菜单中找不到概览选项"
        assert '概览' in options_block, "期权投研菜单中找不到'概览'文本"
        
        print("[OK] 期权投研菜单包含概览选项")

    def test_sidebar_menu_has_collections_option(self):
        """测试期权投研下是否有数据集合选项"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找期权投研菜单块
        options_start = content.find('index="/options"')
        assert options_start > 0, "找不到期权投研菜单"
        
        options_end = content.find('</el-sub-menu>', options_start)
        options_block = content[options_start:options_end]
        
        assert 'index="/options/collections"' in options_block, "期权投研菜单中找不到数据集合选项"
        assert '数据集合' in options_block, "期权投研菜单中找不到'数据集合'文本"
        
        print("[OK] 期权投研菜单包含数据集合选项")

    def test_sidebar_menu_has_analysis_option(self):
        """测试期权投研下是否有期权分析选项"""
        sidebar_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
        )
        sidebar_path = os.path.abspath(sidebar_path)
        
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找期权投研菜单块
        options_start = content.find('index="/options"')
        assert options_start > 0, "找不到期权投研菜单"
        
        options_end = content.find('</el-sub-menu>', options_start)
        options_block = content[options_start:options_end]
        
        assert 'index="/options/analysis"' in options_block, "期权投研菜单中找不到期权分析选项"
        assert '期权分析' in options_block, "期权投研菜单中找不到'期权分析'文本"
        
        print("[OK] 期权投研菜单包含期权分析选项")

    def test_router_has_options_routes(self):
        """测试路由配置是否包含期权投研路由"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'router', 'index.ts'
        )
        router_path = os.path.abspath(router_path)
        
        assert os.path.exists(router_path), f"路由文件不存在: {router_path}"
        
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有 /options 路由
        assert "path: '/options'" in content, "路由配置中找不到 /options 路径"
        
        # 验证有 overview 子路由
        assert "path: 'overview'" in content or "'overview'" in content, "路由配置中找不到 overview 子路由"
        
        # 验证有 collections 子路由  
        assert "path: 'collections'" in content or "'collections'" in content, "路由配置中找不到 collections 子路由"
        
        # 验证有 analysis 子路由
        assert "path: 'analysis'" in content or "'analysis'" in content, "路由配置中找不到 analysis 子路由"
        
        print("[OK] 路由配置包含期权投研相关路由")

    def test_options_overview_page_exists(self):
        """测试期权概览页面文件是否存在"""
        overview_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Options', 'index.vue'
        )
        overview_path = os.path.abspath(overview_path)
        
        assert os.path.exists(overview_path), f"期权概览页面文件不存在: {overview_path}"
        
        print("[OK] 期权概览页面文件存在")

    def test_options_collections_page_exists(self):
        """测试期权数据集合页面文件是否存在"""
        collections_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Options', 'Collections.vue'
        )
        collections_path = os.path.abspath(collections_path)
        
        assert os.path.exists(collections_path), f"期权数据集合页面文件不存在: {collections_path}"
        
        print("[OK] 期权数据集合页面文件存在")

    def test_options_analysis_page_exists(self):
        """测试期权分析页面文件是否存在"""
        analysis_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Options', 'OptionsAnalysis.vue'
        )
        analysis_path = os.path.abspath(analysis_path)
        
        assert os.path.exists(analysis_path), f"期权分析页面文件不存在: {analysis_path}"
        
        print("[OK] 期权分析页面文件存在")

    def test_backend_options_router_exists(self):
        """测试后端期权路由文件是否存在"""
        router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'app', 'routers', 'options.py'
        )
        router_path = os.path.abspath(router_path)
        
        assert os.path.exists(router_path), f"后端期权路由文件不存在: {router_path}"
        
        # 验证路由文件中有基本的API端点定义
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'APIRouter' in content, "路由文件中找不到 APIRouter"
        assert 'router = APIRouter' in content, "路由文件中找不到 router 定义"
        assert '/api/options' in content, "路由文件中找不到 /api/options 前缀"
        
        print("[OK] 后端期权路由文件存在且配置正确")


if __name__ == "__main__":
    # 直接运行所有测试
    import sys
    test = TestOptionsFeature()
    failed = 0
    
    print("="*70)
    print("期权投研功能测试")
    print("="*70)
    
    tests = [
        ('test_sidebar_menu_has_options_button', '侧边栏期权投研菜单'),
        ('test_sidebar_menu_has_overview_option', '概览选项'),
        ('test_sidebar_menu_has_collections_option', '数据集合选项'),
        ('test_sidebar_menu_has_analysis_option', '期权分析选项'),
        ('test_router_has_options_routes', '路由配置'),
        ('test_options_overview_page_exists', '概览页面文件'),
        ('test_options_collections_page_exists', '数据集合页面文件'),
        ('test_options_analysis_page_exists', '期权分析页面文件'),
        ('test_backend_options_router_exists', '后端路由文件'),
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
