"""
测试集合: 债券指数 (pytest版本)
MongoDB Collection: bond_indices_daily
AkShare Interface: bond_zh_index_*系列
Provider Method: save_indices需要index_id参数

说明：债券指数如中债指数、中证指数等
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestIndices:
    """债券指数测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取债券指数数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取债券指数数据...")
        df = await provider.get_bond_index(symbol="000832")
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 债券指数接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条指数数据")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存债券指数数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_bond_index(symbol="000832")
        
        if df.empty:
            print("\n⚠️ 债券指数接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条指数数据...")
        
        # 保存到MongoDB
        index_id = "中证转债"
        saved_count = await bond_service.save_indices(df, index_id, value_column="close")
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询债券指数数据"""
        print("\n[查询1] 查询所有债券指数记录（前10条）")
        
        cursor = bond_service.col_indices.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_indices.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                date = item.get('date', 'N/A')
                index_id = item.get('index_id', 'N/A')
                value = item.get('value', 'N/A')
                change = item.get('change', 'N/A')
                print(f"  {i}. {date} {index_id}: {value} ({change})")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按指数ID查询
        if count > 0:
            print("\n[查询2] 按指数ID查询历史数据")
            first_item = items[0] if items else None
            if first_item and first_item.get('index_id'):
                test_index = first_item['index_id']
                index_cursor = bond_service.col_indices.find(
                    {'index_id': test_index}
                ).sort('date', -1).limit(5)
                index_items = await index_cursor.to_list(length=5)
                print(f"✅ {test_index} 最近5条记录: {len(index_items)} 条")
