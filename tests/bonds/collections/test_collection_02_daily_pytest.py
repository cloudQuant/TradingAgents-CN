"""
测试集合: 债券日线行情 (pytest版本)
MongoDB Collection: bond_daily
AkShare Interface: bond_zh_hs_cov_daily
Provider Method: get_historical_data
"""
import pytest
from datetime import datetime, timedelta
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestBondDaily:
    """债券日线行情测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self, test_bond_codes):
        """测试从AkShare获取数据"""
        provider = AKShareBondProvider()
        
        # 获取最近3个月数据
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
        
        # 尝试多个债券代码直到获取到数据
        df = None
        successful_code = None
        
        for code in test_bond_codes:
            try:
                df = await provider.get_historical_data(
                    code=code,
                    start_date=start_date,
                    end_date=end_date
                )
                if df is not None and not df.empty:
                    successful_code = code
                    break
            except Exception as e:
                print(f"尝试代码 {code} 失败: {e}")
                continue
        
        assert df is not None and not df.empty, f"获取日线数据失败。尝试的代码: {test_bond_codes}, successful_code: {successful_code}"
        
        print(f"\n✅ 成功获取 {len(df)} 条日线数据 (代码: {successful_code})")
        print(f"\n数据样本（前5条）:")
        print(df.head(5))
        
        # 验证关键字段
        required_fields = ['date', 'open', 'high', 'low', 'close', 'volume']
        for field in required_fields:
            assert field in df.columns, f"缺少字段: {field}"
        
        print(f"\n✅ 包含所有关键字段: {', '.join(required_fields)}")
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service, test_bond_codes):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
        
        # 尝试多个代码获取数据
        df = None
        successful_code = None
        for code in test_bond_codes:
            try:
                df = await provider.get_historical_data(
                    code=code,
                    start_date=start_date,
                    end_date=end_date
                )
                if df is not None and not df.empty:
                    successful_code = code
                    break
            except:
                continue
        
        assert df is not None and not df.empty, f"获取日线数据失败，无法测试保存。尝试的代码: {test_bond_codes}"
        
        print(f"\n准备保存 {len(df)} 条日线数据 (代码: {successful_code})...")
        saved_count = await bond_service.save_historical_data(df, code=successful_code)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service, test_bond_code):
        """测试从MongoDB查询数据"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"\n[查询1] 查询最近30天数据")
        result = await bond_service.query_historical_data(
            code=test_bond_code,
            start_date=start_date,
            end_date=end_date
        )
        
        assert result is not None, "查询结果为None"
        total = result.get('total', 0)
        items = result.get('items', [])
        
        if total > 0:
            print(f"✅ 查询成功，共 {total} 条数据")
            for i, item in enumerate(items[:3], 1):
                date = item.get('date', 'N/A')
                close = item.get('close', 'N/A')
                volume = item.get('volume', 'N/A')
                print(f"  {i}. 日期:{date} 收盘:{close} 成交量:{volume}")
        
        # 查询最新一条
        print(f"\n[查询2] 查询最新一条数据")
        result_latest = await bond_service.query_historical_data(
            code=test_bond_code,
            limit=1
        )
        
        if result_latest and result_latest.get('total', 0) > 0:
            latest = result_latest['items'][0]
            print(f"✅ 最新数据: 日期={latest.get('date')} 收盘={latest.get('close')}")
        
        assert total > 0 or result_latest.get('total', 0) > 0, "查询失败：数据库中无数据"
