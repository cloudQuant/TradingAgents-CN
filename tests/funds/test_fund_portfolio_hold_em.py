#!/usr/bin/env python3
"""
基金持仓-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundPortfolioHoldEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_portfolio_hold_em_data(self, db_connection):
        """测试保存和清空基金持仓"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '基金代码': '000001',
                '股票代码': '600519',
                '股票名称': '贵州茅台',
                '季度': '2024Q3',
                '持仓占比': 8.50,
                '持仓数量': 1000000,
                '持仓市值': 1850000000
            },
            {
                '基金代码': '000001',
                '股票代码': '000858',
                '股票名称': '五粮液',
                '季度': '2024Q3',
                '持仓占比': 6.30,
                '持仓数量': 800000,
                '持仓市值': 950000000
            },
            {
                '基金代码': '000001',
                '股票代码': '600519',
                '股票名称': '贵州茅台',
                '季度': '2024Q2',
                '持仓占比': 8.20,
                '持仓数量': 950000,
                '持仓市值': 1700000000
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_portfolio_hold_em_data(test_data)
        assert saved_count == 3
        
        # 获取统计
        stats = await service.get_fund_portfolio_hold_em_stats()
        assert stats['total_count'] == 3
        
        # 清空数据
        deleted_count = await service.clear_fund_portfolio_hold_em_data()
        assert deleted_count == 3


class TestFundPortfolioHoldEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试基金持仓集合端点"""
        # 测试集合列表包含基金持仓
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_portfolio_hold_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_portfolio_hold_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_portfolio_hold_em/stats")
        assert response.status_code == 200
        
        # 测试单个基金刷新
        response = await test_client.post(
            "/api/funds/collections/fund_portfolio_hold_em/refresh",
            json={"fund_code": "000001", "date": "2024-09-30"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self, test_client):
        """测试单个更新和批量更新"""
        # 单个更新（需要日期参数）
        response = await test_client.post(
            "/api/funds/collections/fund_portfolio_hold_em/refresh",
            json={"fund_code": "000001", "date": "2024-09-30"}
        )
        assert response.status_code == 200
        
        # 批量更新（需要日期参数）
        response = await test_client.post(
            "/api/funds/collections/fund_portfolio_hold_em/refresh",
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
