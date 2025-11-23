#!/usr/bin/env python3
"""
场内交易基金排行-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundExchangeRankEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_exchange_rank_em_data(self, db_connection):
        """测试保存和清空场内交易基金排行数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '159915',
                '基金简称': '易方达创业板ETF',
                '类型': 'ETF',
                '日期': '2024-01-15',
                '单位净值': 2.5000,
                '累计净值': 2.5000,
                '近1周': 1.20,
                '近1月': 3.50,
                '近3月': 8.00,
                '近6月': 15.00,
                '近1年': 25.00,
                '近2年': 45.00,
                '近3年': 65.00,
                '今年来': 12.00,
                '成立来': 150.00,
                '成立日期': '2011-09-20'
            },
            {
                '序号': 2,
                '基金代码': '512880',
                '基金简称': '证券ETF',
                '类型': 'ETF',
                '日期': '2024-01-15',
                '单位净值': 1.3000,
                '累计净值': 1.3000,
                '近1周': 2.30,
                '近1月': 5.00,
                '近3月': 10.00,
                '近6月': 18.00,
                '近1年': 30.00,
                '近2年': 50.00,
                '近3年': 70.00,
                '今年来': 15.00,
                '成立来': 30.00,
                '成立日期': '2015-07-06'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_exchange_rank_em_data(test_data)
        assert saved_count == 2
        
        # 获取统计
        stats = await service.get_fund_exchange_rank_em_stats()
        assert stats['total_count'] == 2
        
        # 清空数据
        deleted_count = await service.clear_fund_exchange_rank_em_data()
        assert deleted_count == 2


class TestFundExchangeRankEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试场内交易基金排行集合端点"""
        # 测试集合列表包含场内交易基金排行
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_exchange_rank_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_exchange_rank_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_exchange_rank_em/stats")
        assert response.status_code == 200
        
        # 测试刷新
        response = await test_client.post("/api/funds/collections/fund_exchange_rank_em/refresh", json={})
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
