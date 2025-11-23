#!/usr/bin/env python3
"""
持有人结构-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundHoldStructureEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_hold_structure_em_data(self):
        """测试保存和清空持有人结构"""
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
                    '机构持有比例': 60.5,
                    '个人持有比例': 39.5,
                    '内部持有比例': 0.0,
                    '总份额': 1500000000.0,
                    'code': '000001'
                },
                {
                    '截止日期': '2023-12-31',
                    '机构持有比例': 65.5,
                    '个人持有比例': 34.5,
                    '内部持有比例': 0.0,
                    '总份额': 1600000000.0,
                    'code': '000001'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_hold_structure_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_hold_structure_em_stats()
            assert stats['total_count'] == 2
            assert stats['unique_funds'] == 1
            
            # 清空数据
            deleted_count = await service.clear_fund_hold_structure_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundHoldStructureEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试持有人结构集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含持有人结构
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_hold_structure_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_hold_structure_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_hold_structure_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh (single)
                mock_df = pd.DataFrame([
                    {
                        '截止日期': '2023-06-30',
                        '机构持有比例': 60.5,
                        '个人持有比例': 39.5,
                        '内部持有比例': 0.0,
                        '总份额': 1500000000.0,
                        'code': '000001'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_hold_structure_em', return_value=mock_df):
                    # 测试单个刷新
                    response = await client.post(
                        "/api/funds/collections/fund_hold_structure_em/refresh",
                        json={'code': '000001'}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
