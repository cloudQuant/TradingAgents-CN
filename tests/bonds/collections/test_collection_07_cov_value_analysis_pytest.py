"""
测试集合: 可转债价值分析 (pytest版本)
MongoDB Collection: bond_cb_valuation_daily
AkShare Interface: bond_zh_cov_value_analysis
Provider Method: get_cov_value_analysis
"""
import pytest
from datetime import datetime, timedelta
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestCovValueAnalysis:
    """可转债价值分析测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self, test_bond_code):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        print(f"正在获取可转债 {test_bond_code} 的价值分析数据...")
        df = await provider.get_cov_value_analysis(code=test_bond_code)
        
        assert df is not None, "获取的数据为None"
        assert not df.empty, "获取的数据为空"
        
        print(f"\n✅ 成功获取 {len(df)} 条价值分析历史数据")
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 统计溢价率
        if '转股溢价率' in df.columns and '纯债溢价率' in df.columns:
            try:
                import pandas as pd
                
                premium_conv = pd.to_numeric(df['转股溢价率'], errors='coerce').dropna()
                if len(premium_conv) > 0:
                    print(f"\n转股溢价率统计:")
                    print(f"  最小值: {premium_conv.min():.2f}%")
                    print(f"  最大值: {premium_conv.max():.2f}%")
                    print(f"  平均值: {premium_conv.mean():.2f}%")
                
                premium_bond = pd.to_numeric(df['纯债溢价率'], errors='coerce').dropna()
                if len(premium_bond) > 0:
                    print(f"\n纯债溢价率统计:")
                    print(f"  最小值: {premium_bond.min():.2f}%")
                    print(f"  最大值: {premium_bond.max():.2f}%")
                    print(f"  平均值: {premium_bond.mean():.2f}%")
            except Exception as e:
                print(f"⚠️  统计时出错: {e}")
        
        # 验证关键字段
        key_fields = ['日期', '收盘价', '纯债价值', '转股价值', '纯债溢价率', '转股溢价率']
        available_fields = [f for f in key_fields if f in df.columns]
        print(f"\n包含关键字段: {', '.join(available_fields)}")
        
        assert len(df) > 30, f"数据量太少: {len(df)}条，预期至少30条"
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service, test_bond_code):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        df = await provider.get_cov_value_analysis(code=test_bond_code)
        
        assert df is not None and not df.empty, "无数据可保存"
        
        print(f"\n准备保存 {len(df)} 条价值分析数据...")
        saved_count = await bond_service.save_cov_value_analysis(test_bond_code, df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service, test_bond_code):
        """测试从MongoDB查询数据"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"\n[查询1] 查询最近30天价值分析")
        
        result = await bond_service.query_cov_value_analysis(
            code=test_bond_code,
            start_date=start_date,
            end_date=end_date
        )
        
        total = result.get('total', 0) if result else 0
        
        if total == 0:
            # 尝试查询所有历史数据
            print("未找到最近30天数据，尝试查询所有历史数据...")
            result = await bond_service.query_cov_value_analysis(
                code=test_bond_code,
                limit=10
            )
            total = result.get('total', 0) if result else 0
        
        if total > 0:
            print(f"✅ 查询成功，共 {total} 条数据")
            items = result.get('items', [])
            for i, item in enumerate(items[:3], 1):
                date = item.get('日期', item.get('date', 'N/A'))
                close = item.get('收盘价', item.get('close', 'N/A'))
                conv_value = item.get('转股价值', item.get('conversion_value', 'N/A'))
                conv_premium = item.get('转股溢价率', item.get('conversion_premium', 'N/A'))
                print(f"  {i}. {date}: 收盘={close} 转股价值={conv_value} 溢价率={conv_premium}%")
        
        # 查询最新数据
        print(f"\n[查询2] 查询最新一条数据")
        result_latest = await bond_service.query_cov_value_analysis(
            code=test_bond_code,
            limit=1
        )
        
        if result_latest and result_latest.get('total', 0) > 0:
            latest = result_latest['items'][0]
            date = latest.get('日期', latest.get('date', 'N/A'))
            close = latest.get('收盘价', latest.get('close', 'N/A'))
            print(f"✅ 最新数据: 日期={date} 收盘价={close}")
        
        assert total > 0, "查询失败"
