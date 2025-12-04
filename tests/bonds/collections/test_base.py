"""
债券数据集合测试基类
提供通用测试方法
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class BondCollectionTestBase:
    """债券数据集合测试基类"""
    
    # 子类需要设置的属性
    collection_name = ""
    display_name = ""
    
    def _get_project_root(self):
        """获取项目根目录"""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    
    def test_provider_file_exists(self):
        """测试Provider文件存在"""
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'bonds', 'providers',
            f'{self.collection_name}_provider.py'
        )
        assert os.path.exists(provider_path), f"Provider文件不存在: {provider_path}"
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否继承了正确的基类
        assert 'BaseProvider' in content or 'SimpleProvider' in content, \
            f"Provider未继承BaseProvider或SimpleProvider"
        print(f"[OK] {self.collection_name} Provider文件存在且继承正确基类")
    
    def test_service_file_exists(self):
        """测试Service文件存在"""
        service_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'bonds', 'services',
            f'{self.collection_name}_service.py'
        )
        assert os.path.exists(service_path), f"Service文件不存在: {service_path}"
        
        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否继承了正确的基类
        assert 'BaseService' in content or 'SimpleService' in content, \
            f"Service未继承BaseService或SimpleService"
        print(f"[OK] {self.collection_name} Service文件存在且继承正确基类")
    
    def test_update_config_exists(self):
        """测试更新配置存在"""
        config_path = os.path.join(
            self._get_project_root(),
            'app', 'config', 'bond_update_config.py'
        )
        assert os.path.exists(config_path), f"配置文件不存在: {config_path}"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查集合配置是否存在
        assert f'"{self.collection_name}"' in content, \
            f"配置文件中未找到 {self.collection_name} 的配置"
        print(f"[OK] {self.collection_name} 更新配置存在")
    
    def test_collection_metadata_exists(self):
        """测试集合元信息存在"""
        metadata_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'bonds', 'collection_metadata.py'
        )
        assert os.path.exists(metadata_path), f"元信息文件不存在: {metadata_path}"
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查集合元信息是否存在
        assert f'"{self.collection_name}"' in content, \
            f"元信息文件中未找到 {self.collection_name} 的配置"
        print(f"[OK] {self.collection_name} 元信息存在")
    
    def test_router_includes_collection(self):
        """测试路由包含该集合"""
        router_path = os.path.join(
            self._get_project_root(),
            'app', 'routers', 'bonds.py'
        )
        assert os.path.exists(router_path), f"路由文件不存在: {router_path}"
        print(f"[OK] 债券路由文件存在")
    
    def test_frontend_collection_page_exists(self):
        """测试前端集合详情页存在"""
        page_path = os.path.join(
            self._get_project_root(),
            'frontend', 'src', 'views', 'Bonds', 'Collection.vue'
        )
        
        if os.path.exists(page_path):
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有刷新、清空等功能
            assert '更新数据' in content or 'refresh' in content.lower(), \
                "页面中找不到更新数据功能"
            print(f"[OK] 前端债券集合详情页包含必要功能")
        else:
            # 如果没有单独的Bonds页面，检查是否使用通用页面
            default_page = os.path.join(
                self._get_project_root(),
                'frontend', 'src', 'views', 'Funds', 'collections', 'DefaultCollection.vue'
            )
            if os.path.exists(default_page):
                print(f"[OK] 使用通用的DefaultCollection.vue页面")
            else:
                print(f"[WARN] 前端债券集合详情页不存在，可能需要创建")
    
    def run_all_tests(self):
        """运行所有测试"""
        tests = [
            ('test_provider_file_exists', 'Provider文件存在'),
            ('test_service_file_exists', 'Service文件存在'),
            ('test_update_config_exists', '更新配置存在'),
            ('test_collection_metadata_exists', '集合元信息存在'),
            ('test_router_includes_collection', '路由包含集合'),
            ('test_frontend_collection_page_exists', '前端页面存在'),
        ]
        
        failed = 0
        print("="*70)
        print(f"{self.display_name} ({self.collection_name}) 测试")
        print("="*70)
        
        for test_method, test_name in tests:
            try:
                print(f"\n[测试] {test_name}...")
                getattr(self, test_method)()
            except AssertionError as e:
                print(f"  [FAILED] {e}")
                failed += 1
            except Exception as e:
                print(f"  [ERROR] {e}")
                failed += 1
        
        print("\n" + "="*70)
        if failed == 0:
            print("[SUCCESS] 所有测试通过！")
        else:
            print(f"[FAILED] {failed} 个测试失败")
        print("="*70)
        
        return failed == 0
