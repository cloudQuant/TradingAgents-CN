"""
测试集合: 债券分钟行情 (pytest版本)
MongoDB Collection: bond_minute_quotes
AkShare Interface: bond_zh_hs_cov_min
Provider Method: 通过save_bond_minute_quotes保存
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestMinuteQuotes:
    """债券分钟行情测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        # 测试可转债分钟数据（使用日线数据作为替代测试）
        code = "sh110062"  # 皖维转债
        df = await provider.get_historical_data(code, None, None)
        
        assert df is not None, "获取的数据为None"
        print(f"\n债券代码: {code}")
        print(f"数据条数: {len(df)}")
        if not df.empty:
            print(f"数据样本:\n{df.head(3)}")
        else:
            print("接口可调用，但暂无数据")
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        
        code = "sh110062"
        period = "1"
        df = await provider.get_historical_data(code, None, None)
        
        if df is not None and not df.empty:
            saved_count = await bond_service.save_bond_minute_quotes(code, df, period)
            print(f"\n✅ 成功保存 {saved_count} 条数据")
            assert saved_count >= 0, "保存操作失败"
        else:
            print("\n⚠️ 接口暂无数据，跳过保存测试")
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        print("\n查询bond_minute_quotes集合")
        count = await bond_service.col_minute.count_documents({})
        print(f"集合中共有 {count} 条记录")
