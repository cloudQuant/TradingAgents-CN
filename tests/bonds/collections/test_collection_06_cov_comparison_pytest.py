"""
测试集合: 可转债比价表 (pytest版本)
MongoDB Collection: bond_cb_comparison
AkShare Interface: bond_cov_comparison
Provider Method: get_cov_comparison

注意：该API可能因网络或限流返回空数据，已添加skip标记
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestCovComparison:
    """可转债比价表测试类"""
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="bond_cov_comparison API返回空数据（网络或限流问题），暂时跳过")
    async def test_fetch_data(self):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        print("正在获取东方财富可转债比价表...")
        df = await provider.get_cov_comparison()
        
        assert df is not None, "获取的数据为None"
        assert not df.empty, "获取的数据为空"
        
        print(f"\n✅ 成功获取 {len(df)} 条可转债比价数据")
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 统计转股溢价率分布
        if '转股溢价率' in df.columns:
            try:
                import pandas as pd
                premium_col = df['转股溢价率']
                premium_numeric = pd.to_numeric(premium_col, errors='coerce')
                premium_valid = premium_numeric.dropna()
                
                if len(premium_valid) > 0:
                    print(f"\n转股溢价率统计:")
                    print(f"  最小值: {premium_valid.min():.2f}%")
                    print(f"  最大值: {premium_valid.max():.2f}%")
                    print(f"  平均值: {premium_valid.mean():.2f}%")
                    
                    low_premium = (premium_valid < 10).sum()
                    mid_premium = ((premium_valid >= 10) & (premium_valid < 30)).sum()
                    high_premium = (premium_valid >= 30).sum()
                    print(f"\n溢价率分布:")
                    print(f"  <10%: {low_premium}只")
                    print(f"  10-30%: {mid_premium}只")
                    print(f"  ≥30%: {high_premium}只")
            except Exception as e:
                print(f"⚠️  统计转股溢价率时出错: {e}")
        
        assert len(df) > 100, f"数据量太少: {len(df)}条"
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="bond_cov_comparison API返回空数据（网络或限流问题），暂时跳过")
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        df = await provider.get_cov_comparison()
        
        assert df is not None and not df.empty, "无数据可保存"
        
        print(f"\n准备保存 {len(df)} 条可转债比价数据...")
        saved_count = await bond_service.save_cov_comparison(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="bond_cov_comparison API返回空数据（网络或限流问题），暂时跳过")
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        print(f"\n[查询1] 查询所有可转债（前10条）")
        
        result = await bond_service.query_cov_comparison(
            page=1,
            page_size=10
        )
        
        assert result is not None, "查询结果为None"
        total = result.get('total', 0)
        items = result.get('items', [])
        
        if total > 0:
            print(f"✅ 查询成功，共 {total} 条数据")
            for i, item in enumerate(items[:3], 1):
                code = item.get('转债代码', item.get('code', 'N/A'))
                name = item.get('转债名称', item.get('name', 'N/A'))
                price = item.get('转债最新价', item.get('price', 'N/A'))
                premium = item.get('转股溢价率', item.get('premium_rate', 'N/A'))
                print(f"  {i}. {code} {name}: 价格={price} 溢价率={premium}%")
        
        # 关键词搜索
        print(f"\n[查询2] 搜索'转债'")
        result_search = await bond_service.query_cov_comparison(
            keyword="转债",
            page=1,
            page_size=5
        )
        
        if result_search and result_search.get('total', 0) > 0:
            print(f"✅ 搜索到 {result_search['total']} 条结果")
        
        assert total > 0, "查询失败"
