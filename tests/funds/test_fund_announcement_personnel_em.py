#!/usr/bin/env python3
"""
基金公告人事调整-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundAnnouncementPersonnelEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_announcement_personnel_em_data(self):
        """测试保存和清空基金公告人事调整"""
        from app.services.fund_data_service import FundDataService
        from app.core.database import init_database, close_database, get_mongo_db
        
        await init_database()
        try:
            db = get_mongo_db()
            service = FundDataService(db)
            
            # 创建测试数据
            test_data = pd.DataFrame([
                {
                    'code': '000001',
                    '公告标题': '关于基金经理变更的公告',
                    '公告日期': '2023-06-30',
                    '公告内容': '...'
                },
                {
                    'code': '000002',
                    '公告标题': '关于高级管理人员变更的公告',
                    '公告日期': '2023-06-29',
                    '公告内容': '...'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_announcement_personnel_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_announcement_personnel_em_stats()
            assert stats['total_count'] == 2
            assert stats['unique_funds'] == 2
            
            # 清空数据
            deleted_count = await service.clear_fund_announcement_personnel_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundAnnouncementPersonnelEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试基金公告人事调整集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含基金公告人事调整
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_announcement_personnel_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_announcement_personnel_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_announcement_personnel_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        'code': '000001',
                        '公告标题': '关于基金经理变更的公告',
                        '公告日期': '2023-06-30'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_announcement_personnel_em', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_announcement_personnel_em/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
