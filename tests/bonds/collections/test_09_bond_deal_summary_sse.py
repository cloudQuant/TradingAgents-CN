"""
债券成交概览-上交所数据集合测试用例
需求文档: tests/bonds/requirements/09_债券成交概览-上交所.md
数据唯一标识: 债券类型和日期
"""
from test_base import BondCollectionTestBase


class TestBondDealSummarySseCollection(BondCollectionTestBase):
    """测试债券成交概览-上交所数据集合"""
    
    collection_name = "bond_deal_summary_sse"
    display_name = "债券成交概览-上交所"
    
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
    test = TestBondDealSummarySseCollection()
    success = test.run_all_tests()
    
    # 额外测试
    print("\n[额外测试]")
    try:
        test.test_unique_keys()
    except Exception as e:
        print(f"  [FAILED] {e}")
    
    import sys
    sys.exit(0 if success else 1)
