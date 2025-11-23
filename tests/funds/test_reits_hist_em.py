#!/usr/bin/env python3
"""
REITs历史行情-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestReitsHistEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_reits_hist_em_data(self):
        """测试保存和清空REITs历史行情"""
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
                    'open': 4.110,
                    'close': 4.180,
                    'high': 4.199,
                    'low': 4.110,
                    'volume': 10000,
                    'amount': 41800.0,
                    'adjust': '',
                    'code': '508026'
                },
                {
                    'date': '2023-06-29',
                    'open': 4.000,
                    'close': 4.110,
                    'high': 4.120,
                    'low': 4.000,
                    'volume': 9000,
                    'amount': 36000.0,
                    'adjust': '',
                    'code': '508026'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_reits_hist_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_reits_hist_em_stats()
            assert stats['total_count'] == 2
            assert stats['unique_codes'] == 1
            
            # 清空数据
            deleted_count = await service.clear_reits_hist_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestReitsHistEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试REITs历史行情集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含REITs历史行情
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'reits_hist_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/reits_hist_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/reits_hist_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh (single)
                mock_df = pd.DataFrame([
                    {
                        'date': '2023-06-30',
                        'open': 4.110,
                        'close': 4.180,
                        'high': 4.199,
                        'low': 4.110,
                        'volume': 10000,
                        'amount': 41800.0,
                        'adjust': '',
                        'code': '508026'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_reits_hist_em', return_value=mock_df):
                    # 测试单个刷新
                    response = await client.post(
                        "/api/funds/collections/reits_hist_em/refresh",
                        json={'code': '508026'}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
