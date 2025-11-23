#!/usr/bin/env python3
"""
债券持仓-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundPortfolioBondHoldEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_portfolio_bond_hold_em_data(self, db_connection):
        """测试保存和清空债券持仓"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '基金代码': '000001',
                '债券代码': '019666',
                '债券名称': '22国债14',
                '季度': '2024Q3',
                '持仓占比': 5.50,
                '持仓数量': 5000000,
                '持仓市值': 500000000
            },
            {
                '基金代码': '000001',
                '债券代码': '019658',
                '债券名称': '21国债09',
                '季度': '2024Q3',
                '持仓占比': 4.30,
                '持仓数量': 4000000,
                '持仓市值': 400000000
            },
            {
                '基金代码': '000001',
                '债券代码': '019666',
                '债券名称': '22国债14',
                '季度': '2024Q2',
                '持仓占比': 5.20,
                '持仓数量': 4800000,
                '持仓市值': 480000000
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_portfolio_bond_hold_em_data(test_data)
        assert saved_count == 3
        
        # 获取统计
        stats = await service.get_fund_portfolio_bond_hold_em_stats()
        assert stats['total_count'] == 3
        
        # 清空数据
        deleted_count = await service.clear_fund_portfolio_bond_hold_em_data()
        assert deleted_count == 3


class TestFundPortfolioBondHoldEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试债券持仓集合端点"""
        # 测试集合列表包含债券持仓
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_portfolio_bond_hold_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_portfolio_bond_hold_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_portfolio_bond_hold_em/stats")
        assert response.status_code == 200
        
        # 测试单个基金刷新
        response = await test_client.post(
            "/api/funds/collections/fund_portfolio_bond_hold_em/refresh",
            json={"fund_code": "000001", "date": "2024-09-30"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self, test_client):
        """测试单个更新和批量更新"""
        # 单个更新（需要日期参数）
        response = await test_client.post(
            "/api/funds/collections/fund_portfolio_bond_hold_em/refresh",
            json={"fund_code": "000001", "date": "2024-09-30"}
        )
        assert response.status_code == 200
        
        # 批量更新（需要日期参数）
        response = await test_client.post(
            "/api/funds/collections/fund_portfolio_bond_hold_em/refresh",
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
