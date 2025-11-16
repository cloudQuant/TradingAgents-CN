"""
测试集合: 债券成交概览 (pytest版本)
MongoDB Collection: bond_deal_summary
AkShare Interface: bond_deal_summary_sse
Provider Method: get_deal_summary
"""
import pytest
from datetime import datetime, timedelta
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


async def find_recent_trading_day(provider, max_days=10):
    """查找最近的交易日
    
    Args:
        provider: AKShareBondProvider实例
        max_days: 最多向前查找的天数
        
    Returns:
        tuple: (date_str, dataframe) 或 (None, None)
    """
    for i in range(1, max_days + 1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
        df = await provider.get_deal_summary(date)
        if df is not None and not df.empty:
            return date, df
    return None, None


class TestDealSummary:
    """债券成交概览测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        # 自动查找最近的交易日（最多向前查找10天）
        print("\n正在查找最近的交易日...")
        date, df = await find_recent_trading_day(provider, max_days=10)
        
        if date is None or df is None:
            pytest.skip("未找到最近10天内的交易日数据")
        
        print(f"\n✅ 成功获取 {len(df)} 条成交概览数据 (日期: {date})")
        print(f"\n数据样本（前3条）:")
        print(df.head(3))
        print(f"\n字段列表: {list(df.columns)}")
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        
        # 自动查找最近的交易日
        print("\n正在查找最近的交易日...")
        date, df = await find_recent_trading_day(provider, max_days=10)
        
        if date is None or df is None:
            pytest.skip("未找到最近10天内的交易日数据")
        
        print(f"\n准备保存 {len(df)} 条成交概览数据...")
        saved_count = await bond_service.save_deal_summary(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        # 由于没有专门的query方法，这里简单验证数据存在
        print("✅ 查询bond_deal_summary集合")
        # 可以直接查询collection验证
        count = await bond_service.col_deal_summary.count_documents({})
        print(f"集合中共有 {count} 条记录")
        
        # 如果没有数据，可能是因为之前的测试被跳过
        if count == 0:
            pytest.skip("集合中暂无数据（可能是非交易日）")
