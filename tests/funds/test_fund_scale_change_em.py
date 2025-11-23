#!/usr/bin/env python3
"""
规模变动-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundScaleChangeEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_scale_change_em_data(self):
        """测试保存和清空规模变动"""
        from app.services.fund_data_service import FundDataService
        from app.core.database import init_database, close_database, get_mongo_db
        
        await init_database()
        try:
            db = get_mongo_db()
            service = FundDataService(db)
            
            # 创建测试数据
            test_data = pd.DataFrame([
                {
                    '截止日期': '2023-06-30',
                    '净资产': 2000000000.0,
                    '期间申购': 100000000.0,
                    '期间赎回': 50000000.0,
                    '期末总份额': 1500000000.0,
                    'code': '000001'
                },
                {
                    '截止日期': '2023-03-31',
                    '净资产': 1900000000.0,
                    '期间申购': 80000000.0,
                    '期间赎回': 40000000.0,
                    '期末总份额': 1450000000.0,
                    'code': '000001'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_scale_change_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_scale_change_em_stats()
            assert stats['total_count'] == 2
            assert stats['unique_funds'] == 1
            
            # 清空数据
            deleted_count = await service.clear_fund_scale_change_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundScaleChangeEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试规模变动集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含规模变动
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_scale_change_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_scale_change_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_scale_change_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh (single)
                mock_df = pd.DataFrame([
                    {
                        '截止日期': '2023-06-30',
                        '净资产': 2000000000.0,
                        '期间申购': 100000000.0,
                        '期间赎回': 50000000.0,
                        '期末总份额': 1500000000.0,
                        'code': '000001'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_scale_change_em', return_value=mock_df):
                    # 测试单个刷新
                    response = await client.post(
                        "/api/funds/collections/fund_scale_change_em/refresh",
                        json={'code': '000001'}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
