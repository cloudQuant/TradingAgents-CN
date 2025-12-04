"""
债券查询-中国外汇交易中心数据集合测试用例
需求文档: tests/bonds/requirements/01_债券查询-中国外汇交易中心.md
"""
from test_base import BondCollectionTestBase


class TestBondInfoCmCollection(BondCollectionTestBase):
    """测试债券查询-中国外汇交易中心数据集合"""
    
    collection_name = "bond_info_cm"
    display_name = "债券查询-中国外汇交易中心"
    
    def test_unique_keys(self):
        """测试唯一键配置正确"""
        import os
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'bonds', 'providers',
            f'{self.collection_name}_provider.py'
        )
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根据需求文档，唯一键应为"查询代码"
        assert 'unique_keys' in content, "Provider中未定义unique_keys"
        assert '查询代码' in content, "唯一键应包含'查询代码'"
        print(f"[OK] 唯一键配置正确")
    
    def test_single_update_params(self):
        """测试单条更新参数配置"""
        import os
        config_path = os.path.join(
            self._get_project_root(),
            'app', 'config', 'bond_update_config.py'
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有必要的参数
        assert '"bond_name"' in content or "'bond_name'" in content, "应支持bond_name参数"
        print(f"[OK] 单条更新参数配置正确")


if __name__ == "__main__":
    test = TestBondInfoCmCollection()
    success = test.run_all_tests()
    
    # 额外测试
    print("\n[额外测试]")
    try:
        test.test_unique_keys()
        test.test_single_update_params()
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    import sys
    sys.exit(0 if success else 1)
