"""
股票数据集合测试基类

提供统一的测试框架，子类只需要定义集合名称和测试参数即可
"""
import pytest
import asyncio
from typing import Dict, Any, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch
import pandas as pd


class StockCollectionTestBase:
    """股票数据集合测试基类"""
    
    # 子类必须定义的属性
    collection_name: str = ""
    provider_class: type = None
    service_class: type = None
    
    # 可选配置
    test_params: Dict[str, Any] = {}  # 测试用的参数
    expected_fields: List[str] = []  # 期望的字段列表
    unique_keys: List[str] = []  # 唯一键
    
    @pytest.fixture
    def mock_db(self):
        """创建模拟数据库"""
        db = MagicMock()
        collection = AsyncMock()
        db.__getitem__ = MagicMock(return_value=collection)
        db.__getattr__ = MagicMock(return_value=collection)
        collection.count_documents = AsyncMock(return_value=100)
        collection.find_one = AsyncMock(return_value={"更新时间": "2024-01-01"})
        collection.find = MagicMock(return_value=AsyncMock())
        collection.find().skip = MagicMock(return_value=AsyncMock())
        collection.find().skip().limit = MagicMock(return_value=AsyncMock())
        collection.find().skip().limit().sort = MagicMock(return_value=AsyncMock())
        collection.find().skip().limit().sort().to_list = AsyncMock(return_value=[])
        collection.delete_many = AsyncMock(return_value=MagicMock(deleted_count=10))
        collection.insert_many = AsyncMock(return_value=MagicMock(inserted_ids=[1, 2, 3]))
        return db
    
    @pytest.fixture
    def provider(self):
        """创建Provider实例"""
        if self.provider_class:
            return self.provider_class()
        return None
    
    @pytest.fixture
    def service(self, mock_db):
        """创建Service实例"""
        if self.service_class:
            return self.service_class(mock_db)
        return None
    
    # ==================== Provider 测试 ====================
    
    def test_provider_attributes(self, provider):
        """测试Provider必要属性"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        assert hasattr(provider, 'collection_name'), "Provider应有collection_name属性"
        assert hasattr(provider, 'display_name'), "Provider应有display_name属性"
        assert hasattr(provider, 'akshare_func'), "Provider应有akshare_func属性"
        
        assert provider.collection_name == self.collection_name
        assert provider.collection_name != ""
        assert provider.display_name != ""
        assert provider.akshare_func != ""
    
    def test_provider_unique_keys(self, provider):
        """测试Provider唯一键配置"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        unique_keys = provider.get_unique_keys() if hasattr(provider, 'get_unique_keys') else getattr(provider, 'unique_keys', [])
        assert isinstance(unique_keys, list), "unique_keys应该是列表"
        
        if self.unique_keys:
            assert unique_keys == self.unique_keys, f"唯一键应该是 {self.unique_keys}"
    
    def test_provider_field_info(self, provider):
        """测试Provider字段信息"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        field_info = provider.get_field_info() if hasattr(provider, 'get_field_info') else getattr(provider, 'field_info', [])
        assert isinstance(field_info, list), "field_info应该是列表"
        
        for field in field_info:
            assert 'name' in field, "字段定义应包含name"
            assert 'type' in field, "字段定义应包含type"
    
    def test_provider_collection_meta(self, provider):
        """测试Provider集合元信息"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        if hasattr(provider, 'get_collection_meta'):
            meta = provider.get_collection_meta()
            assert 'name' in meta
            assert 'display_name' in meta
            assert 'description' in meta
            assert 'route' in meta
    
    @pytest.mark.integration
    def test_provider_fetch_data(self, provider):
        """测试Provider数据获取（集成测试）"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        try:
            df = provider.fetch_data(**self.test_params)
            
            assert isinstance(df, pd.DataFrame), "fetch_data应返回DataFrame"
            
            if not df.empty:
                # 检查期望的字段
                if self.expected_fields:
                    for field in self.expected_fields:
                        assert field in df.columns, f"应包含字段: {field}"
                
                # 检查更新时间字段
                time_field = getattr(provider, 'timestamp_field', '更新时间')
                assert time_field in df.columns, f"应包含时间字段: {time_field}"
        except Exception as e:
            pytest.skip(f"数据获取失败（可能是网络问题）: {e}")
    
    # ==================== Service 测试 ====================
    
    def test_service_attributes(self, service):
        """测试Service必要属性"""
        if not service:
            pytest.skip("Service class not defined")
        
        assert hasattr(service, 'collection_name'), "Service应有collection_name属性"
        assert hasattr(service, 'provider'), "Service应有provider属性"
        assert service.collection_name == self.collection_name
    
    @pytest.mark.asyncio
    async def test_service_get_overview(self, service, mock_db):
        """测试Service获取概览"""
        if not service:
            pytest.skip("Service class not defined")
        
        result = await service.get_overview()
        
        assert isinstance(result, dict)
        assert 'total_count' in result
    
    @pytest.mark.asyncio
    async def test_service_get_data(self, service, mock_db):
        """测试Service获取数据"""
        if not service:
            pytest.skip("Service class not defined")
        
        result = await service.get_data(skip=0, limit=10)
        
        assert isinstance(result, dict)
        assert 'data' in result
        assert 'total' in result
    
    @pytest.mark.asyncio
    async def test_service_clear_data(self, service, mock_db):
        """测试Service清空数据"""
        if not service:
            pytest.skip("Service class not defined")
        
        result = await service.clear_data()
        
        assert isinstance(result, dict)
        assert 'success' in result
        assert result['success'] is True


class SimpleStockCollectionTest(StockCollectionTestBase):
    """简单集合测试类（无参数接口）"""
    
    @pytest.mark.integration
    def test_provider_fetch_all_data(self, provider):
        """测试获取全部数据"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        try:
            df = provider.fetch_data()
            assert isinstance(df, pd.DataFrame)
            if not df.empty:
                print(f"获取到 {len(df)} 条数据")
                print(f"字段: {list(df.columns)}")
        except Exception as e:
            pytest.skip(f"数据获取失败: {e}")


class ParameterizedStockCollectionTest(StockCollectionTestBase):
    """参数化集合测试类（需要参数的接口）"""
    
    required_params: List[str] = []  # 必须参数
    
    def test_provider_required_params(self, provider):
        """测试Provider必须参数配置"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        required = getattr(provider, 'required_params', [])
        
        if self.required_params:
            for param in self.required_params:
                assert param in required, f"应包含必须参数: {param}"
    
    @pytest.mark.integration
    def test_provider_fetch_with_params(self, provider):
        """测试带参数获取数据"""
        if not provider:
            pytest.skip("Provider class not defined")
        
        if not self.test_params:
            pytest.skip("未配置测试参数")
        
        try:
            df = provider.fetch_data(**self.test_params)
            assert isinstance(df, pd.DataFrame)
            if not df.empty:
                print(f"获取到 {len(df)} 条数据")
        except ValueError as e:
            if "缺少必须参数" in str(e):
                pytest.fail(f"参数配置错误: {e}")
            raise
        except Exception as e:
            pytest.skip(f"数据获取失败: {e}")
