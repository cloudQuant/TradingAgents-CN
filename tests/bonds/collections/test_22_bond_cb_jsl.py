"""
可转债实时数据-集思录数据集合测试用例
需求文档: tests/bonds/requirements/22_可转债实时数据-集思录.md
数据唯一标识: 代码
"""
from test_base import BondCollectionTestBase


class TestBondCbJslCollection(BondCollectionTestBase):
    """测试可转债实时数据-集思录数据集合"""
    
    collection_name = "bond_cb_jsl"
    display_name = "可转债实时数据-集思录"
    
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
    test = TestBondCbJslCollection()
    success = test.run_all_tests()
    
    # 额外测试
    print("\n[额外测试]")
    try:
        test.test_unique_keys()
    except Exception as e:
        print(f"  [FAILED] {e}")
    
    import sys
    sys.exit(0 if success else 1)
