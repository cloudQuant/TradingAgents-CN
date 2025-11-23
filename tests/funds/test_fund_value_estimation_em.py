#!/usr/bin/env python3
"""
净值估算-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundValueEstimationEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_value_estimation_em_data(self, db_connection):
        """测试保存和清空净值估算数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '000001',
                '基金名称': '华夏成长',
                '交易日-估算数据-估算值': 1.2500,
                '交易日-估算数据-估算增长率': 1.25,
                '交易日-公布数据-单位净值': 1.2450,
                '交易日-公布数据-日增长率': 1.20,
                '估算偏差': 0.05,
                '交易日-单位净值': 1.2450,
                '交易日': '2024-01-15'
            },
            {
                '序号': 2,
                '基金代码': '000002',
                '基金名称': '华夏回报',
                '交易日-估算数据-估算值': 2.3800,
                '交易日-估算数据-估算增长率': 0.85,
                '交易日-公布数据-单位净值': 2.3750,
                '交易日-公布数据-日增长率': 0.80,
                '估算偏差': 0.05,
                '交易日-单位净值': 2.3750,
                '交易日': '2024-01-15'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_value_estimation_em_data(test_data)
        assert saved_count == 2
        
        # 获取统计
        stats = await service.get_fund_value_estimation_em_stats()
        assert stats['total_count'] == 2
        
        # 清空数据
        deleted_count = await service.clear_fund_value_estimation_em_data()
        assert deleted_count == 2


class TestFundValueEstimationEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试净值估算集合端点"""
        # 测试集合列表包含净值估算
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_value_estimation_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_value_estimation_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_value_estimation_em/stats")
        assert response.status_code == 200
        
        # 测试刷新(支持symbol参数)
        response = await test_client.post(
            "/api/funds/collections/fund_value_estimation_em/refresh",
            json={"symbol": "全部"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_with_symbol(self, test_client):
        """测试不同symbol参数的刷新"""
        symbols = ["股票型", "混合型", "债券型", "指数型"]
        
        for symbol in symbols:
            response = await test_client.post(
                "/api/funds/collections/fund_value_estimation_em/refresh",
                json={"symbol": symbol}
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
