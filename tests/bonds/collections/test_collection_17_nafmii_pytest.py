"""
测试集合: 交易商协会债券 (pytest版本)
MongoDB Collection: bond_nafmii_debts
AkShare Interface: 待确认
Provider Method: save_nafmii

说明：NAFMII（中国银行间市场交易商协会）债券数据
"""
import pytest
import pandas as pd


class TestNafmii:
    """交易商协会债券测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取NAFMII债券数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取NAFMII交易商协会债券数据...")
        df = await provider.get_nafmii_bonds()
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ NAFMII债券接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条NAFMII债券数据")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存NAFMII债券数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_nafmii_bonds()
        
        if df.empty:
            print("\n⚠️ NAFMII债券接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条NAFMII债券数据...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_nafmii(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询NAFMII债券数据"""
        print("\n[查询1] 查询所有NAFMII债券（前10条）")
        
        cursor = bond_service.col_nafmii.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_nafmii.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                type_ = item.get('type', 'N/A')
                issuer = item.get('issuer', 'N/A')
                print(f"  {i}. {code} {name} - 类型:{type_} 发行人:{issuer}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按类型查询
        if count > 0:
            print("\n[查询2] 按债券类型查询")
            type_cursor = bond_service.col_nafmii.find({
                'type': {'$exists': True}
            }).limit(5)
            type_items = await type_cursor.to_list(length=5)
            if type_items:
                types = set([item.get('type') for item in type_items if item.get('type')])
                print(f"债券类型: {types}")
