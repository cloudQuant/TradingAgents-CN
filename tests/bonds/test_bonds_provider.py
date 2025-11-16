"""
测试债券数据提供商
包括：AKShare数据获取功能的测试
"""
import pytest
import asyncio
from unittest.mock import patch, Mock, AsyncMock
import pandas as pd
import numpy as np


@pytest.mark.asyncio
async def test_get_cov_comparison():
    """测试获取可转债比价表"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "序号": 1,
                "转债代码": "113682",
                "转债名称": "益丰转债",
                "转债最新价": 120.50,
                "转股溢价率": 12.00
            }
        ])
        mock_ak.bond_cov_comparison.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_cov_comparison()
            
            # 验证
            assert df is not None
            assert not df.empty
            assert len(df) == 1
    
    print("✅ 测试通过：获取可转债比价表")


@pytest.mark.asyncio
async def test_get_cov_value_analysis():
    """测试获取可转债价值分析"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "日期": "2024-01-01",
                "收盘价": 120.0,
                "纯债价值": 90.0,
                "转股价值": 110.0,
                "转股溢价率": 9.1
            }
        ])
        mock_ak.bond_zh_cov_value_analysis.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_cov_value_analysis("113682")
            
            # 验证
            assert df is not None
            assert not df.empty
            assert "日期" in df.columns or "date" in df.columns
    
    print("✅ 测试通过：获取可转债价值分析")


@pytest.mark.asyncio
async def test_get_spot_deal():
    """测试获取现券市场成交行情"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "债券简称": "23附息国债26",
                "成交净价": 103.20,
                "最新收益率": 2.30,
                "涨跌": -0.80
            }
        ])
        mock_ak.bond_spot_deal.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_spot_deal()
            
            # 验证
            assert df is not None
            assert not df.empty
            assert "债券简称" in df.columns
    
    print("✅ 测试通过：获取现券市场成交行情")


@pytest.mark.asyncio
async def test_get_spot_quote():
    """测试获取现券市场做市报价"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "报价机构": "星展银行(中国)",
                "债券简称": "21进出10",
                "买入净价": 100.34,
                "卖出净价": 102.44
            }
        ])
        mock_ak.bond_spot_quote.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_spot_quote()
            
            # 验证
            assert df is not None
            assert not df.empty
            assert "债券简称" in df.columns
    
    print("✅ 测试通过：获取现券市场做市报价")


@pytest.mark.asyncio
async def test_get_cash_summary():
    """测试获取上交所债券现券市场概览"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "债券现货": "国债",
                "托管只数": 193,
                "托管市值": 6815.47,
                "托管面值": 6758.46,
                "数据日期": "2021-01-11"
            }
        ])
        mock_ak.bond_cash_summary_sse.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_cash_summary("20210111")
            
            # 验证
            assert df is not None
            assert not df.empty
            assert "债券现货" in df.columns
    
    print("✅ 测试通过：获取上交所债券现券市场概览")


@pytest.mark.asyncio
async def test_get_deal_summary():
    """测试获取上交所债券成交概览"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "债券类型": "记账式国债",
                "当日成交笔数": 3685,
                "当日成交金额": 363349.44,
                "数据日期": "2021-01-04"
            }
        ])
        mock_ak.bond_deal_summary_sse.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_deal_summary("20210104")
            
            # 验证
            assert df is not None
            assert not df.empty
            assert "债券类型" in df.columns
    
    print("✅ 测试通过：获取上交所债券成交概览")


@pytest.mark.asyncio
async def test_get_cov_info_detail():
    """测试获取可转债详细信息"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # 创建测试数据
        mock_df = pd.DataFrame([
            {
                "SECURITY_CODE": "123121",
                "SECUCODE": "123121.SZ",
                "债券简称": "楚天转债"
            }
        ])
        mock_ak.bond_zh_cov_info.return_value = mock_df
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_cov_info_detail("123121", "基本信息")
            
            # 验证
            assert df is not None
            assert not df.empty
    
    print("✅ 测试通过：获取可转债详细信息")


@pytest.mark.asyncio
async def test_provider_error_handling():
    """测试数据提供商的错误处理"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare抛出异常
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        mock_ak.bond_cov_comparison.side_effect = Exception("网络错误")
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', side_effect=Exception("网络错误")):
            df = await provider.get_cov_comparison()
            
            # 验证返回空DataFrame
            assert df is not None
            assert df.empty
    
    print("✅ 测试通过：数据提供商错误处理")


@pytest.mark.asyncio
async def test_provider_empty_data():
    """测试数据提供商返回空数据"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # Mock akshare返回空DataFrame
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        mock_ak.bond_cov_comparison.return_value = pd.DataFrame()
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new=AsyncMock(return_value=pd.DataFrame())):
            df = await provider.get_cov_comparison()
            
            # 验证
            assert df is not None
            assert df.empty
    
    print("✅ 测试通过：数据提供商空数据处理")


@pytest.mark.asyncio
async def test_code_normalization_in_provider():
    """测试数据提供商中的代码规范化"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # 测试_symbol_candidates_for_ak方法
    candidates = provider._symbol_candidates_for_ak("113682")
    
    # 验证返回的候选代码列表
    assert isinstance(candidates, list)
    assert len(candidates) > 0
    # 应该包含多种格式
    assert any("sh" in c.lower() for c in candidates)
    assert any("113682" in c for c in candidates)
    
    print("✅ 测试通过：数据提供商代码规范化")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
