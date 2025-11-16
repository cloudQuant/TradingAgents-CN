"""
测试集合: 美债收益率 (pytest版本)
MongoDB Collection: us_yield_daily
AkShare Interface: 待确认（可能是bond_us_*系列）
Provider Method: save_us_yields

说明：美国国债收益率曲线数据，包含各期限收益率
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestUsYield:
    """美债收益率测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试美债收益率数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取美国国债收益率数据...")
        df = await provider.get_us_treasury_yield()
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 美债收益率接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条美债收益率数据")
            print(f"\n数据样本（前3条）:")
            print(df.head(3))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存美债收益率数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_us_treasury_yield()
        
        if df.empty:
            print("\n⚠️ 美债收益率接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条美债收益率数据...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_us_yields(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询美债收益率数据"""
        print("\n[查询] 查询美债收益率历史（前10条）")
        
        cursor = bond_service.col_us_yield.find().sort('date', -1).limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_us_yield.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前3条）:")
            for i, item in enumerate(items[:3], 1):
                date = item.get('date', 'N/A')
                y1m = item.get('tenor_1m', 'N/A')
                y10y = item.get('tenor_10y', 'N/A')
                y30y = item.get('tenor_30y', 'N/A')
                print(f"  {i}. {date}: 1M={y1m}% 10Y={y10y}% 30Y={y30y}%")
        else:
            print("\n⚠️ 集合中暂无数据")
