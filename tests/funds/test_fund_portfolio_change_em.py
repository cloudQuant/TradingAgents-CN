#!/usr/bin/env python3
"""
重大变动-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundPortfolioChangeEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_portfolio_change_em_data(self):
        """测试保存和清空重大变动"""
        from app.services.fund_data_service import FundDataService
        from app.core.database import init_database, close_database, get_mongo_db
        
        await init_database()
        try:
            db = get_mongo_db()
            service = FundDataService(db)
            
            # 创建测试数据
            test_data = pd.DataFrame([
                {
                    '序号': 1,
                    '股票代码': '600519',
                    '股票名称': '贵州茅台',
                    '本期累计买入金额': 50000000,
                    '占期初基金资产净值比例': 5.50,
                    '季度': '2024年2季度',
                    '基金代码': '000001',
                    '指标类型': '买入'
                },
                {
                    '序号': 2,
                    '股票代码': '000858',
                    '股票名称': '五粮液',
                    '本期累计买入金额': 40000000,
                    '占期初基金资产净值比例': 4.30,
                    '季度': '2024年2季度',
                    '基金代码': '000001',
                    '指标类型': '买入'
                },
                {
                    '序号': 1,
                    '股票代码': '600519',
                    '股票名称': '贵州茅台',
                    '本期累计卖出金额': 30000000,
                    '占期初基金资产净值比例': 3.20,
                    '季度': '2024年2季度',
                    '基金代码': '000001',
                    '指标类型': '卖出'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_portfolio_change_em_data(test_data)
            assert saved_count == 3
            
            # 获取统计
            stats = await service.get_fund_portfolio_change_em_stats()
            assert stats['total_count'] == 3
            
            # 清空数据
            deleted_count = await service.clear_fund_portfolio_change_em_data()
            assert deleted_count == 3
        finally:
            await close_database()


class TestFundPortfolioChangeEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试重大变动集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含重大变动
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_portfolio_change_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_portfolio_change_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_portfolio_change_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        '序号': 1,
                        '股票代码': '600519',
                        '股票名称': '贵州茅台',
                        '本期累计买入金额': 50000000,
                        '占期初基金资产净值比例': 5.50,
                        '季度': '2024年2季度',
                        '指标类型': '买入'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_portfolio_change_em', return_value=mock_df):
                    # 测试单个基金刷新
                    response = await client.post(
                        "/api/funds/collections/fund_portfolio_change_em/refresh",
                        json={"fund_code": "000001", "date": "2024"}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self):
        """测试单个更新和批量更新"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Mock akshare return value
                mock_df = pd.DataFrame([
                     {
                        '序号': 1,
                        '股票代码': '600519',
                        '股票名称': '贵州茅台',
                        '本期累计买入金额': 50000000,
                        '占期初基金资产净值比例': 5.50,
                        '季度': '2024年2季度',
                        '指标类型': '买入'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_portfolio_change_em', return_value=mock_df):
                    # 单个更新
                    response = await client.post(
                        "/api/funds/collections/fund_portfolio_change_em/refresh",
                        json={"fund_code": "000001", "date": "2024"}
                    )
                    assert response.status_code == 200
                
                # Mock batch list and detail
                mock_list_df = pd.DataFrame({'基金代码': ['000001', '000002']})
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_name_em', return_value=mock_list_df):
                    with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_portfolio_change_em', return_value=mock_df):
                        # 批量更新
                        response = await client.post(
                            "/api/funds/collections/fund_portfolio_change_em/refresh",
                            json={"batch": True, "limit": 2, "date": "2024"}
                        )
                        assert response.status_code == 200
        finally:
            await close_database()

