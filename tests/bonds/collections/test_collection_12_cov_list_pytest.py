"""
测试集合: 可转债列表 (pytest版本)
MongoDB Collection: bond_cov_list
AkShare Interface: 可能需要扩展或使用其他数据源
Provider Method: 使用get_symbol_list筛选可转债

说明：可转债列表数据可从get_symbol_list中筛选category='convertible'的数据
"""
import pytest
import pandas as pd
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestCovList:
    """可转债列表测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取可转债列表数据
        
        方案：从get_symbol_list中筛选可转债数据
        """
        provider = AKShareBondProvider()
        
        print("\n正在获取债券列表...")
        all_bonds = await provider.get_symbol_list()
        
        # 筛选可转债
        cov_bonds = [b for b in all_bonds if b.get('category') == 'convertible']
        
        assert len(cov_bonds) > 0, "未找到可转债数据"
        
        print(f"\n✅ 找到 {len(cov_bonds)} 只可转债")
        print(f"总债券数: {len(all_bonds)}")
        
        # 转换为DataFrame
        df = pd.DataFrame(cov_bonds)
        
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 验证关键字段
        required_fields = ['code', 'name', 'category']
        for field in required_fields:
            assert field in df.columns, f"缺少必需字段: {field}"
        
        # 统计数据质量
        valid_codes = df['code'].notna().sum()
        print(f"\n有效代码数: {valid_codes}/{len(df)}")
        
        # 可转债数量可能较少，只要有数据即可
        assert len(df) > 0, f"未找到可转债数据"
        print(f"✓ 测试通过，找到 {len(df)} 只可转债")
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存可转债列表到MongoDB"""
        provider = AKShareBondProvider()
        
        # 获取债券列表
        all_bonds = await provider.get_symbol_list()
        
        # 筛选可转债
        cov_bonds = [b for b in all_bonds if b.get('category') == 'convertible']
        df = pd.DataFrame(cov_bonds)
        
        assert not df.empty, "无可转债数据可保存"
        
        print(f"\n准备保存 {len(df)} 条可转债列表数据...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_cov_list(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询可转债列表"""
        print("\n[查询1] 查询所有可转债列表（前10条）")
        
        cursor = bond_service.col_cov_list.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_cov_list.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                category = item.get('category', 'N/A')
                price = item.get('trade', item.get('price', 'N/A'))
                print(f"  {i}. {code} {name} ({category}): 价格={price}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按代码查询
        if count > 0:
            print("\n[查询2] 查询特定可转债")
            # 查询第一个可转债的代码
            first_item = items[0] if items else None
            if first_item and first_item.get('code'):
                test_code = first_item['code']
                result = await bond_service.col_cov_list.find_one({'code': test_code})
                if result:
                    print(f"✅ 成功查询到代码 {test_code}: {result.get('name', 'N/A')}")
                else:
                    print(f"⚠️ 未找到代码 {test_code}")
