"""
债券基础信息-中国外汇交易中心数据集合测试用例
需求文档: tests/bonds/requirements/02_债券基础信息-中国外汇交易中心.md
数据唯一标识: 债券代码
"""
from test_base import BondCollectionTestBase


class TestBondInfoDetailCmCollection(BondCollectionTestBase):
    """测试债券基础信息-中国外汇交易中心数据集合"""
    
    collection_name = "bond_info_detail_cm"
    display_name = "债券基础信息-中国外汇交易中心"
    
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
        
        assert 'unique_keys' in content, "Provider中未定义unique_keys"
        print(f"[OK] 唯一键配置存在")


if __name__ == "__main__":
    test = TestBondInfoDetailCmCollection()
    success = test.run_all_tests()
    
    # 额外测试
    print("\n[额外测试]")
    try:
        test.test_unique_keys()
    except Exception as e:
        print(f"  [FAILED] {e}")
    
    import sys
    sys.exit(0 if success else 1)
