#!/usr/bin/env python3
"""
基金基本概况-东财功能测试用例
"""
import pytest
import pandas as pd


class TestFundOverviewEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_and_clear_fund_overview_em_data(self, db_connection):
        """测试保存和清空基金基本概况"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '基金代码': '000001',
                '基金简称': '华夏成长',
                '基金类型': '混合型',
                '发行日期': '2001-12-18',
                '成立日期': '2001-12-18',
                '基金规模': 50.25,
                '基金管理人': '华夏基金',
                '基金托管人': '中国银行',
                '基金经理': '张三',
                '管理费率': 1.50,
                '托管费率': 0.25,
                '业绩比较基准': '沪深300指数收益率×60%+中证全债指数收益率×40%'
            },
            {
                '基金代码': '110022',
                '基金简称': '易方达消费',
                '基金类型': '股票型',
                '发行日期': '2010-08-20',
                '成立日期': '2010-08-20',
                '基金规模': 120.80,
                '基金管理人': '易方达基金',
                '基金托管人': '建设银行',
                '基金经理': '李四',
                '管理费率': 1.50,
                '托管费率': 0.25,
                '业绩比较基准': '申银万国消费品指数收益率×80%+中证全债指数收益率×20%'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_overview_em_data(test_data)
        assert saved_count == 2
        
        # 获取统计
        stats = await service.get_fund_overview_em_stats()
        assert stats['total_count'] == 2
        
        # 清空数据
        deleted_count = await service.clear_fund_overview_em_data()
        assert deleted_count == 2


class TestFundOverviewEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_collection_endpoints(self, test_client):
        """测试基金基本概况集合端点"""
        # 测试集合列表包含基金基本概况
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_overview_em' in collection_names
        
        # 测试获取数据
        response = await test_client.get("/api/funds/collections/fund_overview_em")
        assert response.status_code == 200
        
        # 测试统计
        response = await test_client.get("/api/funds/collections/fund_overview_em/stats")
        assert response.status_code == 200
        
        # 测试单个基金刷新
        response = await test_client.post(
            "/api/funds/collections/fund_overview_em/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_refresh_single_and_batch(self, test_client):
        """测试单个更新和批量更新"""
        # 单个更新
        response = await test_client.post(
            "/api/funds/collections/fund_overview_em/refresh",
            json={"fund_code": "000001"}
        )
        assert response.status_code == 200
        
        # 批量更新
        response = await test_client.post(
            "/api/funds/collections/fund_overview_em/refresh",
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
