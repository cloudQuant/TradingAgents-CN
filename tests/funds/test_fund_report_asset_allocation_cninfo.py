#!/usr/bin/env python3
"""
基金资产配置-巨潮功能测试用例
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from httpx import AsyncClient

# Mock akshare before it is imported anywhere
sys.modules['akshare'] = MagicMock()

class TestFundReportAssetAllocationCninfoBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_report_asset_allocation_cninfo_data(self):
        """测试保存和清空基金资产配置"""
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
                    '股票占净比': 80.5,
                    '债券占净比': 10.5,
                    '现金占净比': 9.0,
                    '净资产': 2000000000.0,
                    '报告期': '2023-06-30'
                },
                {
                    '基金代码': '000002',
                    '基金简称': '华夏回报',
                    '股票占净比': 60.5,
                    '债券占净比': 30.5,
                    '现金占净比': 9.0,
                    '净资产': 1500000000.0,
                    '报告期': '2023-06-30'
                }
            ])
            
            # 保存数据
            saved_count = await service.save_fund_report_asset_allocation_cninfo_data(test_data)
            assert saved_count == 2
            
            # 获取统计
            stats = await service.get_fund_report_asset_allocation_cninfo_stats()
            assert stats['total_count'] == 2
            
            # 清空数据
            deleted_count = await service.clear_fund_report_asset_allocation_cninfo_data()
            assert deleted_count == 2
        finally:
            await close_database()


class TestFundReportAssetAllocationCninfoAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self):
        """测试基金资产配置集合端点"""
        from app.main import app
        from app.core.database import init_database, close_database
        
        await init_database()
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                # 测试集合列表包含基金资产配置
                response = await client.get("/api/funds/collections")
                assert response.status_code == 200
                data = response.json()
                collection_names = [c['name'] for c in data.get('data', [])]
                assert 'fund_report_asset_allocation_cninfo' in collection_names
                
                # 测试获取数据
                response = await client.get("/api/funds/collections/fund_report_asset_allocation_cninfo")
                assert response.status_code == 200
                
                # 测试统计
                response = await client.get("/api/funds/collections/fund_report_asset_allocation_cninfo/stats")
                assert response.status_code == 200
                
                # Mock akshare return value for refresh
                mock_df = pd.DataFrame([
                    {
                        '基金代码': '000001',
                        '基金简称': '华夏成长',
                        '股票占净比': 80.5,
                        '债券占净比': 10.5,
                        '现金占净比': 9.0,
                        '净资产': 2000000000.0,
                        '报告期': '2023-06-30'
                    }
                ])
                
                with patch('app.services.fund_refresh_service.FundRefreshService._fetch_fund_report_asset_allocation_cninfo', return_value=mock_df):
                    # 测试刷新
                    response = await client.post(
                        "/api/funds/collections/fund_report_asset_allocation_cninfo/refresh",
                        json={'date': '20230630'}
                    )
                    assert response.status_code == 200
                    assert response.json()['saved'] == 1
        finally:
            await close_database()
