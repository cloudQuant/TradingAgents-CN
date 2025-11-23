#!/usr/bin/env python3
"""
货币型基金排行-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundMoneyRankEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_money_rank_em_data(self, db_connection):
        """测试保存和清空货币型基金排行数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '000009',
                '基金简称': '易方达天天理财货币A',
                '日期': '2024-01-15',
                '万份收益': 0.5200,
                '年化收益率7日': 1.92,
                '年化收益率14日': 1.88,
                '年化收益率28日': 1.85,
                '近1月': 0.16,
                '近3月': 0.48,
                '近6月': 0.95,
                '近1年': 1.90,
                '近2年': 3.80,
                '近3年': 5.70,
                '近5年': 9.50,
                '今年来': 0.12,
                '成立来': 35.20,
                '手续费': '0.00%'
            },
            {
                '序号': 2,
                '基金代码': '000053',
                '基金简称': '鹏华增值宝货币',
                '日期': '2024-01-15',
                '万份收益': 0.5100,
                '年化收益率7日': 1.89,
                '年化收益率14日': 1.86,
                '年化收益率28日': 1.83,
                '近1月': 0.15,
                '近3月': 0.47,
                '近6月': 0.93,
                '近1年': 1.87,
                '近2年': 3.75,
                '近3年': 5.62,
                '近5年': 9.37,
                '今年来': 0.11,
                '成立来': 28.50,
                '手续费': '0.00%'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_money_rank_em_data(test_data)
        assert saved_count == 2
        
        # 获取统计
        stats = await service.get_fund_money_rank_em_stats()
        assert stats['total_count'] == 2
        
        # 清空数据
        deleted_count = await service.clear_fund_money_rank_em_data()
        assert deleted_count == 2


class TestFundMoneyRankEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试货币型基金排行集合端点"""
        # 测试集合列表包含货币型基金排行
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_money_rank_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_money_rank_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_money_rank_em/stats")
        assert response.status_code == 200
        
        # 测试刷新
        response = await test_client.post("/api/funds/collections/fund_money_rank_em/refresh", json={})
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
