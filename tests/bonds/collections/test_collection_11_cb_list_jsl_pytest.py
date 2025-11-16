"""
测试集合: 集思录可转债列表 (pytest版本)
MongoDB Collection: bond_cb_list_jsl
Data Source: 集思录 (jisilu.cn)
Provider Method: 需要实现JSL数据源

预期数据结构:
- bond_id: 债券代码 (128139)
- bond_nm: 债券名称 (东财转3)
- price: 转债价格
- premium_rt: 转股溢价率
- rating: 信用评级
"""
import pytest
import pandas as pd


class TestCbListJsl:
    """集思录可转债列表测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取集思录可转债数据
        
        注意：集思录需要独立的数据源
        TODO: 实现JSLProvider类和get_cb_list_jsl方法，接口: https://www.jisilu.cn/data/cbnew/
        
        当前策略：使用AkShare的可转债列表作为替代数据源
        """
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取可转债列表（作为集思录数据的替代）...")
        all_bonds = await provider.get_symbol_list()
        
        # 筛选可转债
        cb_bonds = [b for b in all_bonds if b.get('category') == 'convertible']
        
        assert cb_bonds is not None and len(cb_bonds) > 0, "未获取到可转债数据"
        
        # 转换为DataFrame
        df = pd.DataFrame(cb_bonds)
        
        print(f"\n✅ 成功获取 {len(df)} 只可转债")
        print(f"\n数据样本（前5条）:")
        print(df[['code', 'name', 'category']].head(5) if 'code' in df.columns else df.head(5))
        
        assert len(df) > 0, f"未获取到可转债数据"
        print(f"\n✓ 数据验证通过")
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存集思录可转债数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取可转债数据
        all_bonds = await provider.get_symbol_list()
        cb_bonds = [b for b in all_bonds if b.get('category') == 'convertible']
        
        assert len(cb_bonds) > 0, "无可转债数据可保存"
        
        df = pd.DataFrame(cb_bonds)
        
        print(f"\n准备保存 {len(df)} 条可转债数据...")
        saved_count = await bond_service.save_cb_list_jsl(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询集思录可转债数据"""
        print("\n[查询1] 查询所有集思录可转债（前10条）")
        
        cursor = bond_service.col_cb_list_jsl.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_cb_list_jsl.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前3条）:")
            for i, item in enumerate(items[:3], 1):
                bond_id = item.get('bond_id', 'N/A')
                bond_nm = item.get('bond_nm', 'N/A')
                price = item.get('price', 'N/A')
                premium = item.get('premium_rt', 'N/A')
                rating = item.get('rating', 'N/A')
                print(f"  {i}. {bond_id} {bond_nm}: 价格={price} 溢价率={premium}% 评级={rating}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按溢价率查询
        if count > 0:
            print("\n[查询2] 查询低溢价可转债（溢价率<20%）")
            low_premium_cursor = bond_service.col_cb_list_jsl.find({
                'premium_rt': {'$lt': 20}
            }).limit(5)
            low_premium_items = await low_premium_cursor.to_list(length=5)
            if low_premium_items:
                print(f"✅ 找到 {len(low_premium_items)} 条低溢价可转债")
                for item in low_premium_items:
                    bond_nm = item.get('bond_nm', 'N/A')
                    premium = item.get('premium_rt', 'N/A')
                    print(f"  - {bond_nm}: {premium}%")
            else:
                print("未找到溢价率<20%的可转债")
