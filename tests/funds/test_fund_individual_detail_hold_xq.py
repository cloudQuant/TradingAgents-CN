#!/usr/bin/env python3
"""
基金持仓资产比例-雪球功能测试用例
"""
import pytest
import pandas as pd


class TestFundIndividualDetailHoldXqBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_individual_detail_hold_xq_data(self, db_connection):
        """测试保存和清空基金持仓资产比例"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '资产类型': '股票',
                '仓位占比': 85.30,
                '基金代码': '000001',
                '日期': '2024-09-30'
            },
            {
                '资产类型': '债券',
                '仓位占比': 10.50,
                '基金代码': '000001',
                '日期': '2024-09-30'
            },
            {
                '资产类型': '现金',
                '仓位占比': 4.20,
                '基金代码': '000001',
                '日期': '2024-09-30'
            },
            {
                '资产类型': '股票',
                '仓位占比': 82.45,
                '基金代码': '000001',
                '日期': '2024-06-30'
            },
            {
                '资产类型': '债券',
                '仓位占比': 12.30,
                '基金代码': '000001',
                '日期': '2024-06-30'
            },
            {
                '资产类型': '现金',
                '仓位占比': 5.25,
                '基金代码': '000001',
                '日期': '2024-06-30'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_individual_detail_hold_xq_data(test_data)
        assert saved_count == 6
        
        # 获取统计
        stats = await service.get_fund_individual_detail_hold_xq_stats()
        assert stats['total_count'] == 6
        
        # 清空数据
        deleted_count = await service.clear_fund_individual_detail_hold_xq_data()
        assert deleted_count == 6


class TestFundIndividualDetailHoldXqAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试基金持仓资产比例集合端点"""
        # 测试集合列表包含基金持仓资产比例
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_individual_detail_hold_xq' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_individual_detail_hold_xq")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_individual_detail_hold_xq/stats")
        assert response.status_code == 200
        
        # 测试单个基金刷新（需要日期参数）
        response = await test_client.post(
            "/api/funds/collections/fund_individual_detail_hold_xq/refresh",
            json={"fund_code": "000001", "date": "2024-09-30"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self, test_client):
        """测试单个更新和批量更新"""
        # 单个更新（需要日期参数）
        response = await test_client.post(
            "/api/funds/collections/fund_individual_detail_hold_xq/refresh",
            json={"fund_code": "000001", "date": "2024-09-30"}
        )
        assert response.status_code == 200
        
        # 批量更新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_detail_hold_xq/refresh",
            json={"batch": True, "limit": 10, "date": "2024-09-30"}
        )
        assert response.status_code == 200


@pytest.fixture
async def db_connection():
    """数据库连接fixture"""
    from app.core.database import get_mongo_db
    db = get_mongo_db()
    yield db


@pytest.fixture
async def test_client():
    """测试客户端fixture"""
    from httpx import AsyncClient
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
