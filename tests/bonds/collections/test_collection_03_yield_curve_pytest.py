"""
测试集合: 收益率曲线 (pytest版本)
MongoDB Collection: yield_curve_daily
AkShare Interface: bond_china_yield
Provider Method: get_yield_curve
"""
import pytest
from datetime import datetime, timedelta
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestYieldCurve:
    """收益率曲线测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        # 注意：bond_china_yield API返回的是历史数据（截至2021年），不是实时数据
        # 所以我们不使用日期过滤，获取所有可用数据
        df = await provider.get_yield_curve()
        
        assert df is not None, "获取的数据为None"
        assert not df.empty, "获取的数据为空"
        
        print(f"\n✅ 成功获取 {len(df)} 条收益率曲线数据")
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 统计曲线类型
        if '曲线名称' in df.columns:
            curve_types = df['曲线名称'].value_counts()
            print(f"\n曲线类型统计（前5名）:")
            for curve_name, count in curve_types.head(5).items():
                print(f"  {curve_name}: {count}条")
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        
        # 获取所有可用数据（历史数据）
        df = await provider.get_yield_curve()
        
        assert df is not None and not df.empty, "无数据可保存"
        
        print(f"\n准备保存 {len(df)} 条收益率曲线数据...")
        saved_count = await bond_service.save_yield_curve(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        # 使用实际有数据的日期范围（2020-2021年的历史数据）
        start_date = "2021-01-01"
        end_date = "2021-01-31"
        
        print(f"\n[查询1] 查询2021年1月数据")
        
        # 尝试查询国债收益率曲线
        result = await bond_service.query_yield_curve(
            curve_name="中债国债收益率曲线",
            start_date=start_date,
            end_date=end_date
        )
        
        total = result.get('total', 0) if result else 0
        
        if total == 0:
            # 如果没有结果，尝试不指定曲线名称
            print("未找到指定曲线，尝试查询所有曲线...")
            result = await bond_service.query_yield_curve(
                start_date=start_date,
                end_date=end_date,
                limit=10
            )
            total = result.get('total', 0) if result else 0
        
        if total > 0:
            print(f"✅ 查询成功，共 {total} 条数据")
            items = result.get('items', [])
            for i, item in enumerate(items[:3], 1):
                date = item.get('date', 'N/A')
                curve = item.get('curve_name', 'N/A')
                tenor = item.get('tenor', 'N/A')
                yield_val = item.get('yield', 'N/A')
                print(f"  {i}. 日期:{date} 曲线:{curve} 期限:{tenor} 收益率:{yield_val}%")
        
        # 查询10年期
        print(f"\n[查询2] 查询10年期收益率")
        result_10y = await bond_service.query_yield_curve(
            tenor="10年",
            start_date=start_date,
            end_date=end_date,
            limit=5
        )
        
        if result_10y and result_10y.get('total', 0) > 0:
            print(f"✅ 查询到 {result_10y['total']} 条10年期数据")
        
        assert total > 0, "查询失败"
