#!/usr/bin/env python3
"""
基金规模走势-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundAumTrendEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_aum_trend_em_data(self):
        """测试保存和清空基金规模走势"""
        from app.services.fund_data_service import FundDataService
        from app.core.database import init_database, close_database, get_mongo_db
        
        await init_database()
        try:
            db = get_mongo_db()
            service = FundDataService(db)
            
            # 创建测试数据
            test_data = pd.DataFrame([
                {
                    'date': '2023-06-30',
                    'total_aum': 20000.5,
                    'equity_aum': 5000.1,
                    'hybrid_aum': 6000.2,
                    'bond_aum': 7000.3,
                    'index_aum': 1000.4,
                    'qdii_aum': 500.5,
                    'money_aum': 500.0
                },
                {
                    'date': '2023-03-31',
                    'total_aum': 19000.5,
                    'equity_aum': 4000.1,
                    'hybrid_aum': 5000.2,
                    'bond_aum': 6000.3,
                    'index_aum': 800.4,
                    'qdii_aum': 400.5,
                    'money_aum': 3800.0
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_aum_trend_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_aum_trend_em_stats()
            assert stats['total_count'] == 2
            
            # 清空数据
            deleted_count = await service.clear_fund_aum_trend_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundAumTrendEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试基金规模走势集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含基金规模走势
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_aum_trend_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_aum_trend_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_aum_trend_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        'date': '2023-06-30',
                        'total_aum': 20000.5,
                        'equity_aum': 5000.1,
                        'hybrid_aum': 6000.2,
                        'bond_aum': 7000.3,
                        'index_aum': 1000.4,
                        'qdii_aum': 500.5,
                        'money_aum': 500.0
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_aum_trend_em', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_aum_trend_em/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
