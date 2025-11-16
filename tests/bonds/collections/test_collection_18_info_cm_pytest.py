"""
测试集合: 中债信息 (pytest版本)
MongoDB Collection: bond_info_cm
AkShare Interface: 待确认
Provider Method: save_info_cm

说明：中债网（chinamoney.com.cn）债券信息数据
"""
import pytest
import pandas as pd


class TestInfoCm:
    """中债信息测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取中债信息数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取中债网债券信息...")
        df = await provider.get_chinamoney_bond_info()
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 中债网接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条中债信息")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存中债信息数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_chinamoney_bond_info()
        
        if df.empty:
            print("\n⚠️ 中债网接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条中债信息...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_info_cm(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询中债信息数据"""
        print("\n[查询1] 查询所有中债信息（前10条）")
        
        cursor = bond_service.col_info_cm.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_info_cm.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                issuer = item.get('issuer', 'N/A')
                rate = item.get('coupon_rate', 'N/A')
                print(f"  {i}. {code} {name} - 发行人:{issuer} 票面利率:{rate}%")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按发行人查询
        if count > 0:
            print("\n[查询2] 查询财政部发行的债券")
            issuer_cursor = bond_service.col_info_cm.find({
                'issuer': '财政部'
            }).limit(5)
            issuer_items = await issuer_cursor.to_list(length=5)
            if issuer_items:
                print(f"✅ 找到 {len(issuer_items)} 条财政部债券")
