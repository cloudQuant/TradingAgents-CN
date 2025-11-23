#!/usr/bin/env python3
"""
新发基金-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundNewFoundEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_new_found_em_data(self):
        """测试保存和清空新发基金"""
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
                    '发行公司': '华夏基金',
                    '基金类型': '混合型',
                    '集中认购期': '2023-07-01~2023-07-15',
                    '募集份额': 10.5,
                    '成立日期': '2023-07-20',
                    '基金经理': '王泽实'
                },
                {
                    '基金代码': '000002',
                    '基金简称': '华夏成长2',
                    '发行公司': '华夏基金',
                    '基金类型': '股票型',
                    '集中认购期': '2023-07-01~2023-07-15',
                    '募集份额': 5.5,
                    '成立日期': '2023-07-20',
                    '基金经理': '王泽实'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_new_found_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_new_found_em_stats()
            assert stats['total_count'] == 2
            assert len(stats['type_distribution']) > 0
            
            # 清空数据
            deleted_count = await service.clear_fund_new_found_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundNewFoundEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试新发基金集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含新发基金
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_new_found_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_new_found_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_new_found_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        '基金代码': '000001',
                        '基金简称': '华夏成长',
                        '发行公司': '华夏基金',
                        '基金类型': '混合型',
                        '集中认购期': '2023-07-01~2023-07-15',
                        '募集份额': 10.5,
                        '成立日期': '2023-07-20',
                        '基金经理': '王泽实'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_new_found_em', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_new_found_em/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
