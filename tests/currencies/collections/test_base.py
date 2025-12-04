"""
货币数据集合测试基类
提供通用的测试方法和验证逻辑
"""
import os
import sys
import unittest
from pathlib import Path
from typing import Type, List, Dict, Any, Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class CurrenciesCollectionTestBase(unittest.TestCase):
    """货币数据集合测试基类"""
    
    # 子类需要设置的属性
    collection_name: str = ""
    display_name: str = ""
    provider_class_name: str = ""
    service_class_name: str = ""
    expected_fields: List[str] = []
    unique_keys: List[str] = []
    is_simple_provider: bool = False  # 货币数据都需要api_key参数
    required_params: List[str] = []  # 需要参数的Provider的必需参数
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.providers_path = project_root / "app" / "services" / "data_sources" / "currencies" / "providers"
        cls.services_path = project_root / "app" / "services" / "data_sources" / "currencies" / "services"
        cls.metadata_path = project_root / "app" / "services" / "data_sources" / "currencies" / "collection_metadata.py"
    
    def test_01_provider_file_exists(self):
        """测试Provider文件是否存在"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        provider_file = self.providers_path / f"{self.collection_name}_provider.py"
        self.assertTrue(
            provider_file.exists(),
            f"Provider文件不存在: {provider_file}"
        )
    
    def test_02_service_file_exists(self):
        """测试Service文件是否存在"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        service_file = self.services_path / f"{self.collection_name}_service.py"
        self.assertTrue(
            service_file.exists(),
            f"Service文件不存在: {service_file}"
        )
    
    def test_03_provider_class_exists(self):
        """测试Provider类是否可以正确导入"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.providers.{self.collection_name}_provider"
            module = __import__(module_name, fromlist=[self.provider_class_name])
            provider_class = getattr(module, self.provider_class_name, None)
            self.assertIsNotNone(
                provider_class,
                f"Provider类 {self.provider_class_name} 不存在于模块 {module_name}"
            )
        except ImportError as e:
            self.fail(f"无法导入Provider模块: {e}")
    
    def test_04_service_class_exists(self):
        """测试Service类是否可以正确导入"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.services.{self.collection_name}_service"
            module = __import__(module_name, fromlist=[self.service_class_name])
            service_class = getattr(module, self.service_class_name, None)
            self.assertIsNotNone(
                service_class,
                f"Service类 {self.service_class_name} 不存在于模块 {module_name}"
            )
        except ImportError as e:
            self.fail(f"无法导入Service模块: {e}")
    
    def test_05_provider_has_collection_name(self):
        """测试Provider类是否有collection_name属性"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.providers.{self.collection_name}_provider"
            module = __import__(module_name, fromlist=[self.provider_class_name])
            provider_class = getattr(module, self.provider_class_name)
            
            self.assertTrue(
                hasattr(provider_class, 'collection_name'),
                f"Provider类缺少collection_name属性"
            )
            self.assertEqual(
                provider_class.collection_name,
                self.collection_name,
                f"Provider的collection_name不匹配"
            )
        except ImportError as e:
            self.fail(f"无法导入Provider模块: {e}")
    
    def test_06_provider_has_akshare_func(self):
        """测试Provider类是否有akshare_func属性"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.providers.{self.collection_name}_provider"
            module = __import__(module_name, fromlist=[self.provider_class_name])
            provider_class = getattr(module, self.provider_class_name)
            
            self.assertTrue(
                hasattr(provider_class, 'akshare_func'),
                f"Provider类缺少akshare_func属性"
            )
            self.assertTrue(
                provider_class.akshare_func,
                f"Provider的akshare_func为空"
            )
        except ImportError as e:
            self.fail(f"无法导入Provider模块: {e}")
    
    def test_07_provider_has_unique_keys(self):
        """测试Provider类是否有unique_keys属性"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.providers.{self.collection_name}_provider"
            module = __import__(module_name, fromlist=[self.provider_class_name])
            provider_class = getattr(module, self.provider_class_name)
            
            self.assertTrue(
                hasattr(provider_class, 'unique_keys'),
                f"Provider类缺少unique_keys属性"
            )
            self.assertIsInstance(
                provider_class.unique_keys,
                list,
                f"Provider的unique_keys应该是列表"
            )
        except ImportError as e:
            self.fail(f"无法导入Provider模块: {e}")
    
    def test_08_provider_has_field_info(self):
        """测试Provider类是否有field_info属性"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.providers.{self.collection_name}_provider"
            module = __import__(module_name, fromlist=[self.provider_class_name])
            provider_class = getattr(module, self.provider_class_name)
            
            self.assertTrue(
                hasattr(provider_class, 'field_info'),
                f"Provider类缺少field_info属性"
            )
            self.assertIsInstance(
                provider_class.field_info,
                list,
                f"Provider的field_info应该是列表"
            )
        except ImportError as e:
            self.fail(f"无法导入Provider模块: {e}")
    
    def test_09_service_has_collection_name(self):
        """测试Service类是否有collection_name属性"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            module_name = f"app.services.data_sources.currencies.services.{self.collection_name}_service"
            module = __import__(module_name, fromlist=[self.service_class_name])
            service_class = getattr(module, self.service_class_name)
            
            self.assertTrue(
                hasattr(service_class, 'collection_name'),
                f"Service类缺少collection_name属性"
            )
            self.assertEqual(
                service_class.collection_name,
                self.collection_name,
                f"Service的collection_name不匹配"
            )
        except ImportError as e:
            self.fail(f"无法导入Service模块: {e}")
    
    def test_10_collection_in_metadata(self):
        """测试集合是否在元数据配置中"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            from app.services.data_sources.currencies.collection_metadata import CURRENCY_COLLECTION_METADATA
            
            self.assertIn(
                self.collection_name,
                CURRENCY_COLLECTION_METADATA,
                f"集合 {self.collection_name} 不在元数据配置中"
            )
        except ImportError as e:
            self.fail(f"无法导入元数据配置: {e}")
    
    def test_11_provider_registered(self):
        """测试Provider是否已注册"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            from app.services.data_sources.currencies.provider_registry import get_currency_provider_by_name
            
            provider_class = get_currency_provider_by_name(self.collection_name)
            self.assertIsNotNone(
                provider_class,
                f"Provider {self.collection_name} 未注册"
            )
        except ImportError as e:
            self.fail(f"无法导入Provider注册表: {e}")
    
    def test_12_service_registered(self):
        """测试Service是否已注册"""
        if not self.collection_name:
            self.skipTest("collection_name未设置")
        
        try:
            from app.services.data_sources.currencies.service_registry import get_currency_service_by_name
            
            service_class = get_currency_service_by_name(self.collection_name)
            self.assertIsNotNone(
                service_class,
                f"Service {self.collection_name} 未注册"
            )
        except ImportError as e:
            self.fail(f"无法导入Service注册表: {e}")


def run_collection_test(test_class: Type[CurrenciesCollectionTestBase]) -> unittest.TestResult:
    """运行单个集合的测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    # 运行基类测试（会跳过所有测试，因为collection_name未设置）
    unittest.main()
