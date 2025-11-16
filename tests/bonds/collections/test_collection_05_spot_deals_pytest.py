"""
测试集合: 现券成交行情 (pytest版本)
MongoDB Collection: bond_spot_deals
AkShare Interface: bond_spot_deal
Provider Method: get_spot_deal
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestBondSpotDeals:
    """现券成交行情测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        df = await provider.get_spot_deal()
        
        assert df is not None, "获取的数据为None"
        assert not df.empty, "获取的数据为空"
        
        print(f"\n✅ 成功获取 {len(df)} 条成交行情数据")
        print(f"\n数据样本:")
        print(df.head(3))
        print(f"\n字段列表: {list(df.columns)}")
        
        # 验证至少有一些数据
        assert len(df) > 100, f"数据量太少: {len(df)}条"
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        df = await provider.get_spot_deal()
        
        assert df is not None and not df.empty, "无数据可保存"
        
        print(f"\n准备保存 {len(df)} 条数据...")
        saved_count = await bond_service.save_spot_deals(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        result = await bond_service.query_spot_deals(limit=5)
        
        assert result is not None, "查询结果为None"
        assert result.get('total', 0) > 0, "未能查询到数据"
        
        total = result['total']
        items = result.get('items', [])
        
        print(f"\n✅ 查询成功，共 {total} 条数据")
        for i, item in enumerate(items[:3], 1):
            code = item.get('债券简称', item.get('code', 'N/A'))
            price = item.get('成交净价', item.get('price', 'N/A'))
            yield_rate = item.get('最新收益率', item.get('yield', 'N/A'))
            print(f"  {i}. {code} - 价格:{price} 收益率:{yield_rate}%")
