"""
测试数据集合页面
测试目标：
1. 验证数据集合页面是否存在
2. 验证26个数据集合是否都在页面中展示
3. 验证overview页面中数据集合展示逻辑已被删除
"""
import pytest
import os
import re


class TestCollectionsPage:
    """数据集合页面测试类"""
    
    @pytest.fixture
    def frontend_root(self):
        """获取前端项目根目录"""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'frontend'
        )
    
    @pytest.fixture
    def collections_page_path(self, frontend_root):
        """数据集合页面文件路径"""
        return os.path.join(frontend_root, 'src', 'views', 'Bonds', 'Collections.vue')
    
    @pytest.fixture
    def overview_page_path(self, frontend_root):
        """概览页面文件路径"""
        return os.path.join(frontend_root, 'src', 'views', 'Bonds', 'index.vue')
    
    @pytest.fixture
    def router_path(self, frontend_root):
        """路由配置文件路径"""
        return os.path.join(frontend_root, 'src', 'router', 'index.ts')
    
    @pytest.fixture
    def sidebar_menu_path(self, frontend_root):
        """侧边栏菜单文件路径"""
        return os.path.join(frontend_root, 'src', 'components', 'Layout', 'SidebarMenu.vue')
    
    @pytest.fixture
    def expected_collections(self):
        """26个期望的数据集合名称"""
        return [
            'bond_spot',           # 1. 现券市场行情
            'bond_daily',          # 2. 债券日线行情
            'bond_profiles',       # 3. 债券基本信息
            'bond_buybacks',       # 4. 债券回购利率
            'bond_buybacks_hist',  # 5. 回购历史数据
            'bond_indices',        # 6. 债券指数
            'bond_cb_list',        # 7. 可转债列表
            'bond_cb_list_jsl',    # 8. 可转债列表（集思录）
            'bond_cb_profiles',    # 9. 可转债基本信息
            'bond_cb_summary',     # 10. 可转债汇总
            'bond_cov_list',       # 11. 可转债对比列表
            'bond_cov_comparison', # 12. 可转债比价表
            'bond_nafmii',         # 13. NAFMII债券
            'bond_info_cm',        # 14. 中债网债券信息
            'bond_yield_curve_map', # 15. 收益率曲线映射
            'bond_cb_adjustments', # 16. 可转债调整
            'bond_cb_redeems',     # 17. 可转债赎回
            'bond_issues',         # 18. 债券发行
            'bond_events',         # 19. 债券事件
            'us_yield_daily',      # 20. 美债收益率
            'bond_minute_quotes',  # 21. 债券分钟行情
            'bond_yield_china',    # 22. 中国债券收益率
            'bond_close_return',   # 23. 债券收盘收益
            'bond_index_detail',   # 24. 债券指数详情
            'bond_repo_rates',     # 25. 债券回购利率汇总
            'bond_rating_changes'  # 26. 债券评级变动
        ]
    
    def test_collections_page_exists(self, collections_page_path):
        """测试1：验证数据集合页面文件是否存在"""
        assert os.path.exists(collections_page_path), \
            f"数据集合页面不存在: {collections_page_path}\n" \
            "请创建 frontend/src/views/Bonds/Collections.vue 文件"
    
    def test_collections_page_has_component(self, collections_page_path):
        """测试2：验证数据集合页面是否是一个有效的Vue组件"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证必要的Vue组件结构
        assert '<template>' in content, "缺少 <template> 标签"
        assert '<script' in content, "缺少 <script> 标签"
        assert '</template>' in content, "缺少 </template> 标签"
        assert '</script>' in content, "缺少 </script> 标签"
    
    def test_collections_route_exists(self, router_path):
        """测试3：验证路由配置中是否有数据集合页面的路由"""
        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证路由配置
        assert "path: 'collections'" in content or "path: '/bonds/collections'" in content, \
            "路由配置中缺少数据集合列表页面的路由 (path: 'collections')"
        
        # 验证是否导入了Collections.vue组件
        assert "Collections.vue" in content, \
            "路由配置中缺少对Collections.vue组件的引用"
    
    def test_overview_page_no_collections(self, overview_page_path):
        """测试4：验证overview页面中数据集合展示逻辑已被删除"""
        with open(overview_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否还有数据集合相关的代码
        collections_patterns = [
            r'collections-card',
            r'collections-list',
            r'collection-item',
            r'loadCollections',
            r'viewCollection',
            r'数据集合'
        ]
        
        found_patterns = []
        for pattern in collections_patterns:
            if re.search(pattern, content):
                found_patterns.append(pattern)
        
        assert len(found_patterns) == 0, \
            f"overview页面中仍然包含数据集合相关代码: {found_patterns}\n" \
            "请删除 index.vue 中的数据集合展示逻辑"
    
    def test_collections_page_displays_all_collections(self, collections_page_path, expected_collections):
        """测试5：验证数据集合页面展示所有26个集合"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证页面调用了获取集合列表的API
        assert 'getCollections' in content or 'loadCollections' in content, \
            "页面中缺少获取集合列表的函数调用"
        
        # 验证页面有展示集合列表的逻辑
        assert 'v-for' in content, "页面中缺少列表渲染逻辑 (v-for)"
        
        # 验证页面标题包含"数据集合"
        assert '数据集合' in content, "页面标题中缺少'数据集合'关键词"
    
    def test_collections_page_has_navigation(self, collections_page_path):
        """测试6：验证数据集合页面可以导航到详情页"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有点击事件或路由跳转逻辑
        navigation_patterns = [
            r'@click',
            r'router.push',
            r'navigateTo',
            r'viewCollection'
        ]
        
        has_navigation = any(re.search(pattern, content) for pattern in navigation_patterns)
        assert has_navigation, \
            "数据集合页面缺少导航到详情页的逻辑 (@click 或 router.push)"
    
    def test_collections_page_has_styling(self, collections_page_path):
        """测试7：验证数据集合页面有样式"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有样式定义
        assert '<style' in content, "页面缺少 <style> 标签"
        assert '</style>' in content, "页面缺少 </style> 标签"
    
    def test_collections_page_responsive(self, collections_page_path):
        """测试8：验证数据集合页面响应式布局"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证使用了响应式布局（el-row, el-col或grid）
        responsive_patterns = [
            r'el-row',
            r'el-col',
            r':xs=',
            r':sm=',
            r':md=',
            r':lg=',
            r'grid'
        ]
        
        has_responsive = any(re.search(pattern, content) for pattern in responsive_patterns)
        assert has_responsive, \
            "数据集合页面缺少响应式布局配置 (el-row/el-col 或 grid)"
    
    def test_collections_page_loading_state(self, collections_page_path):
        """测试9：验证数据集合页面有加载状态"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证有loading状态
        assert 'loading' in content.lower(), \
            "数据集合页面缺少加载状态管理 (loading)"
    
    def test_collections_count_display(self, collections_page_path):
        """测试10：验证数据集合页面显示集合数量"""
        with open(collections_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证显示集合总数
        count_patterns = [
            r'collections\.length',
            r'共.*个',
            r'总数',
            r'count'
        ]
        
        has_count = any(re.search(pattern, content) for pattern in count_patterns)
        assert has_count, \
            "数据集合页面缺少集合数量显示"
    
    def test_collections_menu_item_exists(self, sidebar_menu_path):
        """测试11：验证侧边栏菜单中有数据集合菜单项"""
        with open(sidebar_menu_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证菜单项存在
        assert '/bonds/collections' in content, \
            "侧边栏菜单中缺少数据集合菜单项 (/bonds/collections)"
        
        # 验证菜单显示文本
        assert '数据集合' in content, \
            "侧边栏菜单中缺少'数据集合'文本"
        
        # 验证在债券分析子菜单中
        # 检查数据集合菜单项是否在债券分析(bonds)的子菜单区域内
        bonds_section = re.search(
            r'<el-sub-menu index="/bonds">.*?</el-sub-menu>',
            content,
            re.DOTALL
        )
        assert bonds_section, "未找到债券分析子菜单"
        
        bonds_content = bonds_section.group(0)
        assert '/bonds/collections' in bonds_content, \
            "数据集合菜单项不在债券分析子菜单中"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
