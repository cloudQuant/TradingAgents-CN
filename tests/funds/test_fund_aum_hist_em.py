#!/usr/bin/env python3
"""
基金公司历年管理规模-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundAumHistEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_aum_hist_em_data(self):
        """测试保存和清空基金公司历年管理规模"""
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
                    '基金公司': '易方达基金',
                    '总规模': 17000.5,
                    '股票型': 2000.1,
                    '混合型': 3000.2,
                    '债券型': 5000.3,
                    '指数型': 1000.4,
                    'QDII': 500.5,
                    '货币型': 5000.0,
                    '更新日期': '2023-06-30'
                },
                {
                    '序号': 1,
                    '基金公司': '易方达基金',
                    '总规模': 16000.5,
                    '股票型': 1900.1,
                    '混合型': 2900.2,
                    '债券型': 4900.3,
                    '指数型': 900.4,
                    'QDII': 400.5,
                    '货币型': 4900.0,
                    '更新日期': '2022-06-30'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_aum_hist_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_aum_hist_em_stats()
            assert stats['total_count'] == 2
            assert stats['unique_companies'] == 1
            
            # 清空数据
            deleted_count = await service.clear_fund_aum_hist_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundAumHistEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试基金公司历年管理规模集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含基金公司历年管理规模
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_aum_hist_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_aum_hist_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_aum_hist_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        '序号': 1,
                        '基金公司': '易方达基金',
                        '总规模': 17000.5,
                        '股票型': 2000.1,
                        '混合型': 3000.2,
                        '债券型': 5000.3,
                        '指数型': 1000.4,
                        'QDII': 500.5,
                        '货币型': 5000.0,
                        '更新日期': '2023-06-30'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_aum_hist_em', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_aum_hist_em/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
