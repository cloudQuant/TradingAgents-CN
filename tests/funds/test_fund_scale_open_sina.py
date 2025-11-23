#!/usr/bin/env python3
"""
开放式基金规模-新浪功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundScaleOpenSinaBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_scale_open_sina_data(self):
        """测试保存和清空开放式基金规模"""
        from app.services.fund_data_service import FundDataService
        from app.core.database import init_database, close_database, get_mongo_db
        
        await init_database()
        try:
            db = get_mongo_db()
            service = FundDataService(db)
            
            # 创建测试数据
            test_data = pd.DataFrame([
                {
                    '基金代码': '000001',
                    '基金简称': '华夏成长',
                    '管理公司': '华夏基金',
                    '成立日期': '2001-12-18',
                    '最新份额': 30.5,
                    '最新规模': 40.2,
                    '汇率': 1.0,
                    '更新日期': '2023-06-30'
                },
                {
                    '基金代码': '000002',
                    '基金简称': '华夏成长2',
                    '管理公司': '华夏基金',
                    '成立日期': '2001-12-18',
                    '最新份额': 10.5,
                    '最新规模': 20.2,
                    '汇率': 1.0,
                    '更新日期': '2023-06-30'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_scale_open_sina_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_scale_open_sina_stats()
            assert stats['total_count'] == 2
            assert stats['unique_funds'] == 2
            
            # 清空数据
            deleted_count = await service.clear_fund_scale_open_sina_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundScaleOpenSinaAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试开放式基金规模集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含开放式基金规模
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_scale_open_sina' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_scale_open_sina")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_scale_open_sina/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        '基金代码': '000001',
                        '基金简称': '华夏成长',
                        '管理公司': '华夏基金',
                        '成立日期': '2001-12-18',
                        '最新份额': 30.5,
                        '最新规模': 40.2,
                        '汇率': 1.0,
                        '更新日期': '2023-06-30'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_scale_open_sina', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_scale_open_sina/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
