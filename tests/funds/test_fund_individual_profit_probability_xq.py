#!/usr/bin/env python3
"""
基金盈利概率-雪球功能测试用例
"""
import pytest
import pandas as pd


class TestFundIndividualProfitProbabilityXqBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_individual_profit_probability_xq_data(self, db_connection):
        """测试保存和清空基金盈利概率"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '持有时长': '1个月',
                '盈利概率': 55.30,
                '平均收益': 1.25,
                '基金代码': '000001'
            },
            {
                '持有时长': '3个月',
                '盈利概率': 62.80,
                '平均收益': 3.45,
                '基金代码': '000001'
            },
            {
                '持有时长': '6个月',
                '盈利概率': 70.20,
                '平均收益': 7.80,
                '基金代码': '000001'
            },
            {
                '持有时长': '1年',
                '盈利概率': 78.50,
                '平均收益': 15.60,
                '基金代码': '000001'
            },
            {
                '持有时长': '3年',
                '盈利概率': 92.30,
                '平均收益': 52.80,
                '基金代码': '000001'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_individual_profit_probability_xq_data(test_data)
        assert saved_count == 5
        
        # 获取统计
        stats = await service.get_fund_individual_profit_probability_xq_stats()
        assert stats['total_count'] == 5
        
        # 清空数据
        deleted_count = await service.clear_fund_individual_profit_probability_xq_data()
        assert deleted_count == 5


class TestFundIndividualProfitProbabilityXqAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试基金盈利概率集合端点"""
        # 测试集合列表包含基金盈利概率
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_individual_profit_probability_xq' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_individual_profit_probability_xq")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_individual_profit_probability_xq/stats")
        assert response.status_code == 200
        
        # 测试单个基金刷新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_profit_probability_xq/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self, test_client):
        """测试单个更新和批量更新"""
        # 单个更新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_profit_probability_xq/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
        
        # 批量更新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_profit_probability_xq/refresh",
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
