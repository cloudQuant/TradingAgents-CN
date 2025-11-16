"""
测试集合: 现券市场做市报价详情 (pytest版本)
MongoDB Collection: bond_spot_quote_detail
AkShare Interface: bond_spot_quote (扩展)
Provider Method: get_spot_quote
说明：现券做市报价的详细数据，复用get_spot_quote接口
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestSpotQuoteDetail:
    """现券市场做市报价详情测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取现券做市报价详细数据"""
        provider = AKShareBondProvider()
        
        print("正在获取银行间市场做市报价详情...")
        df = await provider.get_spot_quote()
        
        assert df is not None, "获取的数据为None"
        assert not df.empty, "获取的数据为空"
        
        print(f"\n✅ 成功获取 {len(df)} 条做市报价详情数据")
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 打印所有字段
        print(f"\n字段列表: {list(df.columns)}")
        
        # 验证关键字段存在
        expected_fields = ["债券简称", "买入净价", "卖出净价"]
        missing_fields = [f for f in expected_fields if f not in df.columns]
        if missing_fields:
            print(f"⚠️  缺少字段: {missing_fields}")
        else:
            print(f"✓ 所有关键字段都存在")
        
        # 统计数据质量
        if '报价机构' in df.columns:
            institutions = df['报价机构'].value_counts()
            print(f"\n报价机构分布:")
            for inst, count in institutions.head(5).items():
                print(f"  {inst}: {count}条")
        
        assert len(df) > 5, f"数据量太少: {len(df)}条"
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存做市报价详情到MongoDB"""
        provider = AKShareBondProvider()
        df = await provider.get_spot_quote()
        
        assert df is not None and not df.empty, "无数据可保存"
        
        print(f"\n准备保存 {len(df)} 条做市报价详情数据...")
        
        # 使用save_spot_quote_detail方法
        saved_count = await bond_service.save_spot_quote_detail(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询做市报价详情"""
        print("\n[查询1] 查询所有做市报价详情（前10条）")
        
        # 直接查询集合
        cursor = bond_service.col_spot_quote_detail.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_spot_quote_detail.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前3条）:")
            for i, item in enumerate(items[:3], 1):
                institution = item.get('报价机构', item.get('institution', 'N/A'))
                bond_name = item.get('债券简称', item.get('code', 'N/A'))
                bid = item.get('买入净价', item.get('bid_price', 'N/A'))
                ask = item.get('卖出净价', item.get('ask_price', 'N/A'))
                print(f"  {i}. {institution} - {bond_name}: 买入={bid} 卖出={ask}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按字段查询
        if count > 0:
            print("\n[查询2] 查询特定报价机构的报价")
            dealer_cursor = bond_service.col_spot_quote_detail.find(
                {"报价机构": {"$exists": True, "$ne": ""}}
            ).limit(5)
            dealer_items = await dealer_cursor.to_list(length=5)
            if dealer_items:
                print(f"✅ 找到 {len(dealer_items)} 条包含报价机构的记录")
                first_dealer = dealer_items[0].get('报价机构', 'N/A')
                print(f"示例报价机构: {first_dealer}")
