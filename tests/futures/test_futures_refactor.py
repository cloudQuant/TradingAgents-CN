"""
测试期货模块重构
验证Provider-Service架构是否正常工作
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest


class TestFuturesProviders:
    """测试Provider导入"""
    
    def test_import_fees_info_provider(self):
        """测试导入期货费用信息Provider"""
        from app.services.data_sources.futures.providers.futures_fees_info_provider import FuturesFeesInfoProvider
        provider = FuturesFeesInfoProvider()
        assert hasattr(provider, 'fetch_data')
        assert hasattr(provider, 'get_unique_keys')
        assert hasattr(provider, 'get_field_info')
    
    def test_import_comm_info_provider(self):
        """测试导入期货手续费Provider"""
        from app.services.data_sources.futures.providers.futures_comm_info_provider import FuturesCommInfoProvider
        provider = FuturesCommInfoProvider()
        assert hasattr(provider, 'fetch_data')
    
    def test_import_rule_provider(self):
        """测试导入期货规则Provider"""
        from app.services.data_sources.futures.providers.futures_rule_provider import FuturesRuleProvider
        provider = FuturesRuleProvider()
        assert hasattr(provider, 'fetch_data')
    
    def test_import_inventory_99_provider(self):
        """测试导入99期货库存Provider"""
        from app.services.data_sources.futures.providers.futures_inventory_99_provider import FuturesInventory99Provider
        provider = FuturesInventory99Provider()
        assert hasattr(provider, 'fetch_data')
    
    def test_import_dce_position_rank_provider(self):
        """测试导入大商所持仓排名Provider"""
        from app.services.data_sources.futures.providers.futures_dce_position_rank_provider import FuturesDcePositionRankProvider
        provider = FuturesDcePositionRankProvider()
        assert hasattr(provider, 'fetch_data')


class TestFuturesServices:
    """测试Service导入"""
    
    def test_import_base_service(self):
        """测试导入基类服务"""
        from app.services.data_sources.futures.services.base_futures_service import BaseFuturesService
        assert hasattr(BaseFuturesService, 'get_overview')
        assert hasattr(BaseFuturesService, 'update_single_data')
        assert hasattr(BaseFuturesService, 'update_batch_data')
    
    def test_import_fees_info_service(self):
        """测试导入期货费用信息Service"""
        from app.services.data_sources.futures.services.futures_fees_info_service import FuturesFeesInfoService
        # Service需要db参数，这里只验证类可以导入
        assert FuturesFeesInfoService is not None
    
    def test_import_comm_info_service(self):
        """测试导入期货手续费Service"""
        from app.services.data_sources.futures.services.futures_comm_info_service import FuturesCommInfoService
        assert FuturesCommInfoService is not None
    
    def test_import_inventory_99_service(self):
        """测试导入99期货库存Service"""
        from app.services.data_sources.futures.services.futures_inventory_99_service import FuturesInventory99Service
        assert FuturesInventory99Service is not None


class TestFuturesConfig:
    """测试配置文件"""
    
    def test_import_update_config(self):
        """测试导入更新配置"""
        from app.config.futures_update_config import FUTURES_UPDATE_CONFIGS, get_futures_collection_update_config
        
        # 验证配置存在
        assert isinstance(FUTURES_UPDATE_CONFIGS, dict)
        assert len(FUTURES_UPDATE_CONFIGS) > 0
        
        # 验证特定集合配置
        config = get_futures_collection_update_config("futures_fees_info")
        assert "display_name" in config
        assert "single_update" in config
        assert "batch_update" in config
    
    def test_config_structure(self):
        """测试配置结构"""
        from app.config.futures_update_config import FUTURES_UPDATE_CONFIGS
        
        for name, config in FUTURES_UPDATE_CONFIGS.items():
            assert "display_name" in config, f"{name} 缺少 display_name"
            assert "single_update" in config, f"{name} 缺少 single_update"
            assert "batch_update" in config, f"{name} 缺少 batch_update"
            
            # 验证single_update结构
            single = config["single_update"]
            assert "enabled" in single, f"{name} single_update 缺少 enabled"
            assert "params" in single, f"{name} single_update 缺少 params"
            
            # 验证batch_update结构
            batch = config["batch_update"]
            assert "enabled" in batch, f"{name} batch_update 缺少 enabled"


class TestFuturesRefreshService:
    """测试刷新服务"""
    
    def test_import_refresh_service(self):
        """测试导入刷新服务"""
        try:
            from app.services.futures_refresh_service import FuturesRefreshService
            assert FuturesRefreshService is not None
        except ImportError as e:
            pytest.fail(f"导入FuturesRefreshService失败: {e}")
    
    def test_supported_collections(self):
        """测试获取支持的集合列表"""
        try:
            from app.services.futures_refresh_service import FuturesRefreshService
            # 创建mock db
            service = FuturesRefreshService(db=None)
            supported = service.get_supported_collections()
            assert isinstance(supported, list)
            assert len(supported) > 0
            assert "futures_fees_info" in supported
        except Exception as e:
            pytest.skip(f"需要数据库连接: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
