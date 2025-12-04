"""
中债新综合指数数据集合测试用例
需求文档: tests/bonds/requirements/33_中债新综合指数.md
数据唯一标识: 指标、期限和日期
"""
from test_base import BondCollectionTestBase


class TestBondNewCompositeIndexCbondCollection(BondCollectionTestBase):
    """测试中债新综合指数数据集合"""
    
    collection_name = "bond_new_composite_index_cbond"
    display_name = "中债新综合指数"
    
    def test_unique_keys(self):
        """测试唯一键配置正确（指标、期限和日期）"""
        import os
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'bonds', 'providers',
            f'{self.collection_name}_provider.py'
        )
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根据需求文档，唯一键应为"指标类型、期限和日期"
        assert 'unique_keys' in content, "Provider中未定义unique_keys"
        assert '指标类型' in content or 'indicator' in content.lower(), "唯一键应包含'指标类型'"
        assert '期限' in content or 'period' in content.lower(), "唯一键应包含'期限'"
        assert 'date' in content, "唯一键应包含'date'"
        print(f"[OK] 唯一键配置正确: 指标类型、期限、日期")
    
    def test_indicator_options(self):
        """测试指标类型选项配置"""
        import os
        config_path = os.path.join(
            self._get_project_root(),
            'app', 'config', 'bond_update_config.py'
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键的指标选项
        indicators = ["财富", "全价", "净价", "平均市值法久期"]
        for indicator in indicators:
            assert indicator in content, f"应包含指标选项: {indicator}"
        print(f"[OK] 指标类型选项配置正确")
    
    def test_period_options(self):
        """测试期限选项配置"""
        import os
        config_path = os.path.join(
            self._get_project_root(),
            'app', 'config', 'bond_update_config.py'
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键的期限选项
        periods = ["总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上"]
        for period in periods:
            assert period in content, f"应包含期限选项: {period}"
        print(f"[OK] 期限选项配置正确")
    
    def test_akshare_func(self):
        """测试AkShare函数名正确"""
        import os
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'bonds', 'providers',
            f'{self.collection_name}_provider.py'
        )
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'bond_new_composite_index_cbond' in content, \
            "AkShare函数应为bond_new_composite_index_cbond"
        print(f"[OK] AkShare函数名正确")


if __name__ == "__main__":
    test = TestBondNewCompositeIndexCbondCollection()
    success = test.run_all_tests()
    
    # 额外测试
    print("\n[额外测试]")
    extra_tests = [
        ('test_unique_keys', '唯一键配置'),
        ('test_indicator_options', '指标类型选项'),
        ('test_period_options', '期限选项'),
        ('test_akshare_func', 'AkShare函数名'),
    ]
    
    for method, name in extra_tests:
        try:
            print(f"\n[测试] {name}...")
            getattr(test, method)()
        except Exception as e:
            print(f"  [FAILED] {e}")
    
    import sys
    sys.exit(0 if success else 1)
