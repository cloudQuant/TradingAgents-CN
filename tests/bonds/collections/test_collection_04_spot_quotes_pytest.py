"""
测试集合: 现券做市报价 (pytest版本)
MongoDB Collection: bond_spot_quotes
AkShare Interface: bond_spot_quote
Provider Method: get_spot_quote
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestSpotQuotes:
    """现券做市报价测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        print("正在获取银行间市场做市报价...")
        df = await provider.get_spot_quote()
        
        assert df is not None, "获取的数据为None"
        assert not df.empty, "获取的数据为空"
        
        print(f"\n✅ 成功获取 {len(df)} 条做市报价数据")
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 统计报价机构
        if '报价机构' in df.columns:
            institutions = df['报价机构'].value_counts()
            print(f"\n报价机构统计（前5名）:")
            for inst, count in institutions.head(5).items():
                print(f"  {inst}: {count}条报价")
        
        # 验证至少有一些数据（银行间市场报价机构较少，实际可能只有10-20条）
        assert len(df) > 5, f"数据量太少: {len(df)}条"
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        df = await provider.get_spot_quote()
        
        assert df is not None and not df.empty, "无数据可保存"
        
        print(f"\n准备保存 {len(df)} 条做市报价数据...")
        saved_count = await bond_service.save_spot_quotes(df, category="银行间市场")
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        print(f"\n[查询1] 查询最新报价（前10条）")
        
        result = await bond_service.query_spot_quotes(
            category="银行间市场",
            limit=10
        )
        
        assert result is not None, "查询结果为None"
        total = result.get('total', 0)
        items = result.get('items', [])
        
        if total > 0:
            print(f"✅ 查询成功，共 {total} 条数据")
            for i, item in enumerate(items[:3], 1):
                institution = item.get('报价机构', item.get('institution', 'N/A'))
                bond_name = item.get('债券简称', item.get('bond_name', 'N/A'))
                bid_price = item.get('买入净价', item.get('bid_price', 'N/A'))
                ask_price = item.get('卖出净价', item.get('ask_price', 'N/A'))
                print(f"  {i}. {institution} - {bond_name}: 买入={bid_price} 卖出={ask_price}")
        
        # 搜索国债报价
        print(f"\n[查询2] 搜索包含'国债'的报价")
        result_search = await bond_service.query_spot_quotes(
            bond_name="国债",
            category="银行间市场",
            limit=5
        )
        
        if result_search and result_search.get('total', 0) > 0:
            print(f"✅ 搜索到 {result_search['total']} 条国债报价")
        
        assert total > 0, "查询失败"
