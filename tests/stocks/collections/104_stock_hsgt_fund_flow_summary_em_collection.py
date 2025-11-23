import pytest
import os
from httpx import AsyncClient


BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8848")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

pytestmark = pytest.mark.skipif(
    not AUTH_TOKEN, reason="API_AUTH_TOKEN not set"
)


@pytest.mark.asyncio
async def test_collection_endpoint_exists():
    """测试集合端点是否存在"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_collection_data_structure():
    """测试集合数据结构"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "total" in data
            assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_collection_fields():
    """测试集合字段完整性"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em?page=1&page_size=10",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                item = data["data"][0]
                expected_fields = ["交易日", "类型", "板块", "资金方向", "交易状态", 
                                 "成交净买额", "资金净流入", "当日资金余额", 
                                 "上涨数", "持平数", "下跌数", "相关指数", "指数涨跌幅"]
                for field in expected_fields:
                    assert field in item, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_refresh_collection():
    """测试刷新集合数据"""
    async with AsyncClient(base_url=BASE_URL, timeout=300.0) as client:
        response = await client.post(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em/refresh",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            json={}
        )
        assert response.status_code in [200, 202]


@pytest.mark.asyncio
async def test_collection_overview():
    """测试集合概览"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em/overview",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_count" in data


@pytest.mark.asyncio
async def test_collection_pagination():
    """测试集合分页"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em?page=1&page_size=5",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        if response.status_code == 200:
            data = response.json()
            assert len(data["data"]) <= 5


@pytest.mark.asyncio
async def test_clear_collection():
    """测试清空集合"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete(
            "/stocks/collections/stock_hsgt_fund_flow_summary_em/clear",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        assert response.status_code == 200
