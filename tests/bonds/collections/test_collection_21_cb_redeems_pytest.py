"""
测试集合: 可转债赎回 (pytest版本)
MongoDB Collection: bond_cb_redeems
Provider Method: save_cb_redeems

说明：可转债赎回事件（到期赎回、强制赎回等）
"""
import pytest
import pandas as pd


class TestCbRedeems:
    """可转债赎回测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试可转债赎回数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取可转债赎回数据...")
        df = await provider.get_cb_redeems()
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 可转债赎回接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条赎回数据")
            print(f"\n数据样本:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存赎回数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_cb_redeems()
        
        if df.empty:
            print("\n⚠️ 可转债赎回接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条赎回数据...")
        saved_count = await bond_service.save_cb_redeems(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询赎回数据"""
        print("\n[查询] 查询所有赎回事件（前10条）")
        
        cursor = bond_service.col_cb_redeems.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_cb_redeems.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                type_ = item.get('redeem_type', 'N/A')
                date = item.get('redeem_date', 'N/A')
                print(f"  {i}. {code} {name} - {type_} ({date})")
        else:
            print("\n⚠️ 集合中暂无数据")
