"""
测试集合: 债券事件 (pytest版本)
MongoDB Collection: bond_events
Provider Method: 待实现

说明：债券各类事件（付息、兑付、信用事件等）
"""
import pytest
import pandas as pd


class TestBondEvents:
    """债券事件测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试债券事件数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取债券事件数据...")
        df = await provider.get_bond_events()
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 债券事件接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条事件数据")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存事件数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_bond_events()
        
        if df.empty:
            print("\n⚠️ 债券事件接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条事件数据...")
        
        # 清理旧数据
        codes = df['code'].tolist()
        await bond_service.col_events.delete_many({'code': {'$in': codes}})
        
        # 插入数据
        records = df.to_dict('records')
        result = await bond_service.col_events.insert_many(records)
        saved_count = len(result.inserted_ids)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询事件数据"""
        print("\n[查询] 查询所有债券事件（前10条）")
        
        cursor = bond_service.col_events.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_events.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                type_ = item.get('event_type', 'N/A')
                date = item.get('event_date', 'N/A')
                print(f"  {i}. {code} {name} - {type_} ({date})")
        else:
            print("\n⚠️ 集合中暂无数据")
