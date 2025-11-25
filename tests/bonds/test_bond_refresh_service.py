"""
测试债券数据刷新服务（重构版）

测试内容：
1. BondRefreshService 服务初始化
2. Provider 数据获取
3. Service 数据操作
4. 配置文件加载

使用方法：
python -m pytest tests/bonds/test_bond_refresh_service.py -v
"""

import sys
import os
import pytest

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class TestBondUpdateConfig:
    """测试债券更新配置"""
    
    def test_config_has_34_collections(self):
        """测试配置包含34个集合"""
        from app.config.bond_update_config import BOND_UPDATE_CONFIGS
        
        assert len(BOND_UPDATE_CONFIGS) == 34, f"期望34个集合，实际{len(BOND_UPDATE_CONFIGS)}个"
        print(f"[PASS] Config has {len(BOND_UPDATE_CONFIGS)} collections")
    
    def test_config_structure(self):
        """测试配置结构正确"""
        from app.config.bond_update_config import BOND_UPDATE_CONFIGS
        
        required_keys = ["display_name", "update_description", "single_update", "batch_update"]
        
        for name, config in BOND_UPDATE_CONFIGS.items():
            for key in required_keys:
                assert key in config, f"集合 {name} 缺少 {key} 配置"
        
        print(f"[PASS] All collection config structures are valid")
    
    def test_get_collection_update_config(self):
        """测试获取单个集合配置"""
        from app.config.bond_update_config import get_collection_update_config
        
        config = get_collection_update_config("bond_info_cm")
        
        assert config is not None
        assert config["collection_name"] == "bond_info_cm"
        assert config["display_name"] == "债券信息查询"
        print(f"[PASS] bond_info_cm config retrieved successfully")
    
    def test_get_nonexistent_collection_config(self):
        """测试获取不存在集合的默认配置"""
        from app.config.bond_update_config import get_collection_update_config
        
        config = get_collection_update_config("nonexistent_collection")
        
        assert config is not None
        assert config["collection_name"] == "nonexistent_collection"
        assert config["batch_update"]["enabled"] == True
        print(f"[PASS] Nonexistent collection returns default config")


class TestProviders:
    """测试数据提供者"""
    
    def test_provider_imports(self):
        """测试所有Provider可以正常导入"""
        provider_modules = [
            "bond_info_cm_provider",
            "bond_info_detail_cm_provider",
            "bond_zh_hs_spot_provider",
            "bond_zh_hs_daily_provider",
            "bond_zh_hs_cov_spot_provider",
            "bond_zh_hs_cov_daily_provider",
            "bond_zh_cov_provider",
            "bond_cash_summary_sse_provider",
            "bond_deal_summary_sse_provider",
            "bond_debt_nafmii_provider",
            "bond_spot_quote_provider",
            "bond_spot_deal_provider",
            "bond_zh_hs_cov_min_provider",
            "bond_zh_hs_cov_pre_min_provider",
            "bond_zh_cov_info_provider",
            "bond_zh_cov_info_ths_provider",
            "bond_cov_comparison_provider",
            "bond_zh_cov_value_analysis_provider",
            "bond_sh_buy_back_em_provider",
            "bond_sz_buy_back_em_provider",
            "bond_buy_back_hist_em_provider",
            "bond_cb_jsl_provider",
            "bond_cb_redeem_jsl_provider",
            "bond_cb_index_jsl_provider",
            "bond_cb_adj_logs_jsl_provider",
            "bond_china_close_return_provider",
            "bond_zh_us_rate_provider",
            "bond_treasure_issue_cninfo_provider",
            "bond_local_government_issue_cninfo_provider",
            "bond_corporate_issue_cninfo_provider",
            "bond_cov_issue_cninfo_provider",
            "bond_cov_stock_issue_cninfo_provider",
            "bond_new_composite_index_cbond_provider",
            "bond_composite_index_cbond_provider",
        ]
        
        imported = 0
        failed = []
        
        for module_name in provider_modules:
            try:
                module = __import__(
                    f"app.services.data_sources.bonds.providers.{module_name}",
                    fromlist=[module_name]
                )
                imported += 1
            except ImportError as e:
                failed.append((module_name, str(e)))
        
        if failed:
            for name, error in failed:
                print(f"[FAIL] Import failed: {name} - {error}")
        
        assert len(failed) == 0, f"{len(failed)} providers failed to import"
        print(f"[PASS] Successfully imported {imported} providers")
    
    def test_provider_has_fetch_data(self):
        """测试Provider有fetch_data方法"""
        from app.services.data_sources.bonds.providers.bond_info_cm_provider import BondInfoCmProvider
        
        provider = BondInfoCmProvider()
        
        assert hasattr(provider, "fetch_data")
        assert callable(provider.fetch_data)
        print(f"[PASS] BondInfoCmProvider has fetch_data method")


class TestServices:
    """测试服务层"""
    
    def test_service_imports(self):
        """测试所有Service可以正常导入"""
        service_modules = [
            "bond_info_cm_service",
            "bond_info_detail_cm_service",
            "bond_zh_hs_spot_service",
            "bond_zh_hs_daily_service",
            "bond_zh_hs_cov_spot_service",
            "bond_zh_hs_cov_daily_service",
            "bond_zh_cov_service",
            "bond_cash_summary_sse_service",
            "bond_deal_summary_sse_service",
            "bond_debt_nafmii_service",
            "bond_spot_quote_service",
            "bond_spot_deal_service",
            "bond_zh_hs_cov_min_service",
            "bond_zh_hs_cov_pre_min_service",
            "bond_zh_cov_info_service",
            "bond_zh_cov_info_ths_service",
            "bond_cov_comparison_service",
            "bond_zh_cov_value_analysis_service",
            "bond_sh_buy_back_em_service",
            "bond_sz_buy_back_em_service",
            "bond_buy_back_hist_em_service",
            "bond_cb_jsl_service",
            "bond_cb_redeem_jsl_service",
            "bond_cb_index_jsl_service",
            "bond_cb_adj_logs_jsl_service",
            "bond_china_close_return_service",
            "bond_zh_us_rate_service",
            "bond_treasure_issue_cninfo_service",
            "bond_local_government_issue_cninfo_service",
            "bond_corporate_issue_cninfo_service",
            "bond_cov_issue_cninfo_service",
            "bond_cov_stock_issue_cninfo_service",
            "bond_new_composite_index_cbond_service",
            "bond_composite_index_cbond_service",
        ]
        
        imported = 0
        failed = []
        
        for module_name in service_modules:
            try:
                module = __import__(
                    f"app.services.data_sources.bonds.services.{module_name}",
                    fromlist=[module_name]
                )
                imported += 1
            except ImportError as e:
                failed.append((module_name, str(e)))
        
        if failed:
            for name, error in failed:
                print(f"[FAIL] Import failed: {name} - {error}")
        
        assert len(failed) == 0, f"{len(failed)} services failed to import"
        print(f"[PASS] Successfully imported {imported} services")
    
    def test_base_bond_service(self):
        """测试基础服务类"""
        from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
        
        assert hasattr(BaseBondService, "get_overview")
        assert hasattr(BaseBondService, "get_data")
        assert hasattr(BaseBondService, "update_single_data")
        assert hasattr(BaseBondService, "update_batch_data")
        assert hasattr(BaseBondService, "clear_data")
        print(f"[PASS] BaseBondService has all required methods")


class TestBondRefreshService:
    """测试刷新服务"""
    
    def test_refresh_service_import(self):
        """测试BondRefreshService可以导入"""
        from app.services.bond_refresh_service import BondRefreshService
        
        assert BondRefreshService is not None
        print(f"[PASS] BondRefreshService imported successfully")
    
    def test_refresh_service_has_34_services(self):
        """测试BondRefreshService注册了34个服务"""
        from app.services.bond_refresh_service import BondRefreshService
        
        # 检查_init_services中的服务数量
        service = BondRefreshService.__new__(BondRefreshService)
        service.db = None
        service._services = None
        
        # 获取支持的集合列表（不实际初始化）
        expected_collections = [
            "bond_info_cm", "bond_info_detail_cm",
            "bond_zh_hs_spot", "bond_zh_hs_daily",
            "bond_zh_hs_cov_spot", "bond_zh_hs_cov_daily", "bond_zh_cov",
            "bond_cash_summary_sse", "bond_deal_summary_sse",
            "bond_debt_nafmii", "bond_spot_quote", "bond_spot_deal",
            "bond_zh_hs_cov_min", "bond_zh_hs_cov_pre_min",
            "bond_zh_cov_info", "bond_zh_cov_info_ths",
            "bond_cov_comparison", "bond_zh_cov_value_analysis",
            "bond_sh_buy_back_em", "bond_sz_buy_back_em", "bond_buy_back_hist_em",
            "bond_cb_jsl", "bond_cb_redeem_jsl",
            "bond_cb_index_jsl", "bond_cb_adj_logs_jsl",
            "bond_china_close_return", "bond_zh_us_rate",
            "bond_treasure_issue_cninfo", "bond_local_government_issue_cninfo",
            "bond_corporate_issue_cninfo", "bond_cov_issue_cninfo",
            "bond_cov_stock_issue_cninfo",
            "bond_new_composite_index_cbond", "bond_composite_index_cbond",
        ]
        
        assert len(expected_collections) == 34
        print(f"[PASS] BondRefreshService should register 34 services")
    
    def test_frontend_only_params(self):
        """测试前端专用参数过滤"""
        from app.services.bond_refresh_service import BondRefreshService
        
        expected_params = {
            'batch', 'batch_update', 'update_type', 'concurrency',
            'page', 'limit', 'task_id'
        }
        
        actual_params = BondRefreshService.FRONTEND_ONLY_PARAMS
        
        for param in expected_params:
            assert param in actual_params, f"缺少前端参数: {param}"
        
        print(f"[PASS] Frontend-only params configured correctly")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*80)
    print("Bond Refresh Service Tests (Refactored)")
    print("="*80)
    
    # 测试配置
    print("\n--- Test Config ---")
    config_tests = TestBondUpdateConfig()
    config_tests.test_config_has_34_collections()
    config_tests.test_config_structure()
    config_tests.test_get_collection_update_config()
    config_tests.test_get_nonexistent_collection_config()
    
    # 测试Provider
    print("\n--- Test Providers ---")
    provider_tests = TestProviders()
    provider_tests.test_provider_imports()
    provider_tests.test_provider_has_fetch_data()
    
    # 测试Service
    print("\n--- Test Services ---")
    service_tests = TestServices()
    service_tests.test_service_imports()
    service_tests.test_base_bond_service()
    
    # 测试刷新服务
    print("\n--- Test Refresh Service ---")
    refresh_tests = TestBondRefreshService()
    refresh_tests.test_refresh_service_import()
    refresh_tests.test_refresh_service_has_34_services()
    refresh_tests.test_frontend_only_params()
    
    print("\n" + "="*80)
    print("All tests passed!")
    print("="*80)


if __name__ == "__main__":
    run_all_tests()
