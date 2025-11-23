import pytest
import os
from httpx import AsyncClient

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8848")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")
pytestmark = pytest.mark.skipif(not AUTH_TOKEN, reason="API_AUTH_TOKEN not set")

@pytest.mark.asyncio
async def test_collection_endpoint_exists():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/stocks/collections/stock_financial_abstract", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_refresh_collection():
    async with AsyncClient(base_url=BASE_URL, timeout=300.0) as client:
        response = await client.post("/stocks/collections/stock_financial_abstract/refresh", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, json={})
        assert response.status_code in [200, 202]

@pytest.mark.asyncio
async def test_collection_overview():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/stocks/collections/stock_financial_abstract/overview", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_clear_collection():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete("/stocks/collections/stock_financial_abstract/clear", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        assert response.status_code == 200
