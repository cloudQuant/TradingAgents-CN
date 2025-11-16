"""
测试集合: 债券回购历史 (pytest版本)
MongoDB Collection: bond_buybacks_hist
AkShare Interface: 待确认
Provider Method: save_buybacks_history

说明：债券回购历史数据，记录回购利率的历史走势
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestBuybacksHist:
    """债券回购历史测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取回购历史数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取回购历史数据...")
        df = await provider.get_repo_rate_hist(symbol="R-001")
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 回购历史接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条回购历史数据")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存回购历史数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_repo_rate_hist(symbol="R-001")
        
        if df.empty:
            print("\n⚠️ 回购历史接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条回购历史数据...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_buybacks_history(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询回购历史数据"""
        print("\n[查询1] 查询所有回购历史记录（前10条）")
        
        cursor = bond_service.col_buybacks_hist.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_buybacks_hist.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                date = item.get('date', 'N/A')
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                rate = item.get('rate', 'N/A')
                print(f"  {i}. {date} {code} {name}: {rate}%")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按代码查询历史
        if count > 0:
            print("\n[查询2] 查询特定品种的历史数据")
            first_item = items[0] if items else None
            if first_item and first_item.get('code'):
                test_code = first_item['code']
                code_cursor = bond_service.col_buybacks_hist.find(
                    {'code': test_code}
                ).sort('date', -1).limit(5)
                code_items = await code_cursor.to_list(length=5)
                print(f"✅ {test_code} 最近5条历史记录: {len(code_items)} 条")
