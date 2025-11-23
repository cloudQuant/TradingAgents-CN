#!/usr/bin/env python3
"""
灵活配置型基金仓位-乐咕乐股功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundLinghuoPositionLgBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_linghuo_position_lg_data(self):
        """测试保存和清空灵活配置型基金仓位"""
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
                    '仓位': 55.5
                },
                {
                    'date': '2023-06-29',
                    '仓位': 55.0
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_linghuo_position_lg_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_linghuo_position_lg_stats()
            assert stats['total_count'] == 2
            
            # 清空数据
            deleted_count = await service.clear_fund_linghuo_position_lg_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundLinghuoPositionLgAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试灵活配置型基金仓位集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含灵活配置型基金仓位
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_linghuo_position_lg' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_linghuo_position_lg")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_linghuo_position_lg/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        'date': '2023-06-30',
                        '仓位': 55.5
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_linghuo_position_lg', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_linghuo_position_lg/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
