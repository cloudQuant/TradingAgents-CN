#!/usr/bin/env python3
"""
基金业绩-雪球功能测试用例
"""
import pytest
import pandas as pd


class TestFundIndividualAchievementXqBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_individual_achievement_xq_data(self, db_connection):
        """测试保存和清空基金业绩数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '业绩类型': '年度业绩',
                '周期': '成立以来',
                '本产品区间收益': 399.458300,
                '本产品最大回撒': 54.55,
                '周期收益同类排名': '128/7671',
                '基金代码': '000001'
            },
            {
                '业绩类型': '年度业绩',
                '周期': '今年以来',
                '本产品区间收益': -0.768251,
                '本产品最大回撒': 26.58,
                '周期收益同类排名': '4175/7674',
                '基金代码': '000001'
            },
            {
                '业绩类型': '年度业绩',
                '周期': '2023',
                '本产品区间收益': -21.990000,
                '本产品最大回撒': 26.58,
                '周期收益同类排名': '1631/1843',
                '基金代码': '000001'
            },
            {
                '业绩类型': '季度业绩',
                '周期': '2024-Q1',
                '本产品区间收益': 5.50,
                '本产品最大回撒': 3.20,
                '周期收益同类排名': '500/7000',
                '基金代码': '000002'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_individual_achievement_xq_data(test_data)
        assert saved_count == 4
        
        # 获取统计
        stats = await service.get_fund_individual_achievement_xq_stats()
        assert stats['total_count'] == 4
        assert stats['unique_funds'] == 2
        
        # 清空数据
        deleted_count = await service.clear_fund_individual_achievement_xq_data()
        assert deleted_count == 4


class TestFundIndividualAchievementXqAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试基金业绩集合端点"""
        # 测试集合列表包含基金业绩
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_individual_achievement_xq' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_individual_achievement_xq")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_individual_achievement_xq/stats")
        assert response.status_code == 200
        
        # 测试刷新(需要fund_code参数)
        response = await test_client.post(
            "/api/funds/collections/fund_individual_achievement_xq/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_batch_refresh(self, test_client):
        """测试批量刷新"""
        response = await test_client.post(
            "/api/funds/collections/fund_individual_achievement_xq/refresh",
            json={"batch": True, "limit": 10}
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
