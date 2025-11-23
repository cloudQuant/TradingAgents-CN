#!/usr/bin/env python3
"""
基金数据分析-雪球功能测试用例
"""
import pytest
import pandas as pd


class TestFundIndividualAnalysisXqBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_individual_analysis_xq_data(self, db_connection):
        """测试保存和清空基金数据分析"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '周期': '近一年',
                '较同类风险收益比': 0.85,
                '较同类抗风险波动': 1.15,
                '年化波动率': 15.25,
                '年化夏普比率': 1.42,
                '最大回撤': -12.50,
                '基金代码': '000001'
            },
            {
                '周期': '近三年',
                '较同类风险收益比': 0.92,
                '较同类抗风险波动': 1.08,
                '年化波动率': 16.80,
                '年化夏普比率': 1.35,
                '最大回撤': -18.75,
                '基金代码': '000001'
            },
            {
                '周期': '近五年',
                '较同类风险收益比': 0.78,
                '较同类抗风险波动': 1.22,
                '年化波动率': 14.50,
                '年化夏普比率': 1.55,
                '最大回撤': -22.30,
                '基金代码': '000001'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_individual_analysis_xq_data(test_data)
        assert saved_count == 3
        
        # 获取统计
        stats = await service.get_fund_individual_analysis_xq_stats()
        assert stats['total_count'] == 3
        
        # 清空数据
        deleted_count = await service.clear_fund_individual_analysis_xq_data()
        assert deleted_count == 3


class TestFundIndividualAnalysisXqAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试基金数据分析集合端点"""
        # 测试集合列表包含基金数据分析
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_individual_analysis_xq' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_individual_analysis_xq")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_individual_analysis_xq/stats")
        assert response.status_code == 200
        
        # 测试单个基金刷新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_analysis_xq/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self, test_client):
        """测试单个更新和批量更新"""
        # 单个更新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_analysis_xq/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
        
        # 批量更新
        response = await test_client.post(
            "/api/funds/collections/fund_individual_analysis_xq/refresh",
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
