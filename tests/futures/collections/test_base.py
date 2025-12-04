"""
期货数据集合测试基类
提供通用测试方法
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class FuturesCollectionTestBase:
    """期货数据集合测试基类"""
    
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
            'app', 'services', 'data_sources', 'futures', 'providers',
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
            'app', 'services', 'data_sources', 'futures', 'services',
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
            'app', 'config', 'futures_update_config.py'
        )
        assert os.path.exists(config_path), f"配置文件不存在: {config_path}"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查集合配置是否存在
        if f'"{self.collection_name}"' in content or f"'{self.collection_name}'" in content:
            print(f"[OK] {self.collection_name} 更新配置存在")
        else:
            print(f"[WARN] {self.collection_name} 更新配置未找到，可能使用默认配置")
    
    def test_collection_metadata_exists(self):
        """测试集合元信息存在"""
        metadata_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'futures', 'collection_metadata.py'
        )
        assert os.path.exists(metadata_path), f"元信息文件不存在: {metadata_path}"
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查集合元信息是否存在
        assert f"'{self.collection_name}'" in content or f'"{self.collection_name}"' in content, \
            f"元信息文件中未找到 {self.collection_name} 的配置"
        print(f"[OK] {self.collection_name} 元信息存在")
    
    def test_router_file_exists(self):
        """测试路由文件存在"""
        router_path = os.path.join(
            self._get_project_root(),
            'app', 'routers', 'futures.py'
        )
        assert os.path.exists(router_path), f"路由文件不存在: {router_path}"
        print(f"[OK] 期货路由文件存在")
    
    def test_provider_has_required_attributes(self):
        """测试Provider有必要的属性"""
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'futures', 'providers',
            f'{self.collection_name}_provider.py'
        )
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必要的属性
        assert 'collection_name' in content, "Provider中未定义collection_name"
        assert 'display_name' in content, "Provider中未定义display_name"
        assert 'unique_keys' in content or 'field_info' in content, \
            "Provider中未定义unique_keys或field_info"
        print(f"[OK] Provider包含必要属性")
    
    def run_all_tests(self):
        """运行所有测试"""
        tests = [
            ('test_provider_file_exists', 'Provider文件存在'),
            ('test_service_file_exists', 'Service文件存在'),
            ('test_update_config_exists', '更新配置存在'),
            ('test_collection_metadata_exists', '集合元信息存在'),
            ('test_router_file_exists', '路由文件存在'),
            ('test_provider_has_required_attributes', 'Provider属性完整'),
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
