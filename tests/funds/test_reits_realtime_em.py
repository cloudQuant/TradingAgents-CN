#!/usr/bin/env python3
"""
REITs实时行情-东财功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestReitsRealtimeEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_reits_realtime_em_data(self):
        """测试保存和清空REITs实时行情"""
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
                    '代码': '508026',
                    '名称': '嘉实中国电建清洁能源REIT',
                    '最新价': 4.180,
                    '涨跌额': 0.01,
                    '涨跌幅': 0.24,
                    '成交量': 10000,
                    '成交额': 41800.0,
                    '开盘价': 4.110,
                    '最高价': 4.199,
                    '最低价': 4.110,
                    '昨收': 4.150
                },
                {
                    '序号': 2,
                    '代码': '508009',
                    '名称': '中金安徽交控REIT',
                    '最新价': 7.749,
                    '涨跌额': 0.02,
                    '涨跌幅': 0.26,
                    '成交量': 20000,
                    '成交额': 154980.0,
                    '开盘价': 7.722,
                    '最高价': 7.781,
                    '最低价': 7.687,
                    '昨收': 7.722
                }
            ])
            
            # 保存数据
            saved_count = await service.save_reits_realtime_em_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_reits_realtime_em_stats()
            assert stats['total_count'] == 2
            assert stats['unique_codes'] == 2
            
            # 清空数据
            deleted_count = await service.clear_reits_realtime_em_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestReitsRealtimeEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试REITs实时行情集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含REITs实时行情
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'reits_realtime_em' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/reits_realtime_em")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/reits_realtime_em/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        '序号': 1,
                        '代码': '508026',
                        '名称': '嘉实中国电建清洁能源REIT',
                        '最新价': 4.180,
                        '涨跌额': 0.01,
                        '涨跌幅': 0.24,
                        '成交量': 10000,
                        '成交额': 41800.0,
                        '开盘价': 4.110,
                        '最高价': 4.199,
                        '最低价': 4.110,
                        '昨收': 4.150
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_reits_realtime_em', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/reits_realtime_em/refresh",
                        json={}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
