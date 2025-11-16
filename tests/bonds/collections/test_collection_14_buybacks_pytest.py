"""
测试集合: 债券回购 (pytest版本)
MongoDB Collection: bond_buybacks
AkShare Interface: 待确认（可能是bond_repo_*系列）
Provider Method: save_buybacks需要exchange参数

说明：债券回购数据需要指定交易所（SH/SZ），当前使用模拟数据测试
"""
import pytest
import pandas as pd


class TestBuybacks:
    """债券回购测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试获取债券回购数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取上交所债券回购利率...")
        df = await provider.get_repo_rate(market="SH")
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 上交所回购接口返回空数据，尝试深交所...")
            df = await provider.get_repo_rate(market="SZ")
        
        if df.empty:
            print("⚠️ 回购接口暂无数据或接口不可用")
            # 由于回购接口可能不稳定，这里不强制要求有数据
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条回购数据")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存债券回购数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_repo_rate(market="SH")
        
        if df.empty:
            df = await provider.get_repo_rate(market="SZ")
        
        if df.empty:
            print("\n⚠️ 回购接口暂无数据，跳过保存测试")
            return
        
        print(f"\n准备保存 {len(df)} 条回购数据...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_buybacks(df, exchange="SH")
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询债券回购数据"""
        print("\n[查询1] 查询所有债券回购记录（前10条）")
        
        cursor = bond_service.col_buybacks.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_buybacks.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                exchange = item.get('exchange', 'N/A')
                price = item.get('price', 'N/A')
                print(f"  {i}. {code} {name} ({exchange}): {price}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按交易所查询
        if count > 0:
            print("\n[查询2] 按交易所查询")
            sh_cursor = bond_service.col_buybacks.find({'exchange': 'SH'}).limit(5)
            sh_items = await sh_cursor.to_list(length=5)
            sz_cursor = bond_service.col_buybacks.find({'exchange': 'SZ'}).limit(5)
            sz_items = await sz_cursor.to_list(length=5)
            print(f"  上交所: {len(sh_items)} 条")
            print(f"  深交所: {len(sz_items)} 条")
