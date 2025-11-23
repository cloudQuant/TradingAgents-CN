#!/usr/bin/env python3
"""
香港基金排行-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundHkRankEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_hk_rank_em_data(self, db_connection):
        """测试保存和清空香港基金排行数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '968001',
                '基金简称': '南方全球精选配置',
                '币种': 'USD',
                '日期': '2024-01-15',
                '单位净值': 1.2500,
                '日增长率': 0.50,
                '近1周': 1.20,
                '近1月': 2.50,
                '近3月': 5.80,
                '近6月': 10.20,
                '近1年': 18.50,
                '近2年': 35.20,
                '近3年': 52.30,
                '今年来': 1.20,
                '成立来': 125.00,
                '可购买': '开放申购',
                '香港基金代码': 'HK968001'
            },
            {
                '序号': 2,
                '基金代码': '968002',
                '基金简称': '华夏港股通精选',
                '币种': 'HKD',
                '日期': '2024-01-15',
                '单位净值': 10.8500,
                '日增长率': 0.45,
                '近1周': 1.10,
                '近1月': 2.30,
                '近3月': 5.50,
                '近6月': 9.80,
                '近1年': 17.20,
                '近2年': 32.50,
                '近3年': 48.60,
                '今年来': 1.15,
                '成立来': 108.50,
                '可购买': '开放申购',
                '香港基金代码': 'HK968002'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_hk_rank_em_data(test_data)
        assert saved_count == 2
        
        # 获取统计
        stats = await service.get_fund_hk_rank_em_stats()
        assert stats['total_count'] == 2
        
        # 清空数据
        deleted_count = await service.clear_fund_hk_rank_em_data()
        assert deleted_count == 2


class TestFundHkRankEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试香港基金排行集合端点"""
        # 测试集合列表包含香港基金排行
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_hk_rank_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_hk_rank_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_hk_rank_em/stats")
        assert response.status_code == 200
        
        # 测试刷新
        response = await test_client.post("/api/funds/collections/fund_hk_rank_em/refresh", json={})
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
