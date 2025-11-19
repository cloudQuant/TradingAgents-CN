"""股票数据集合数据接口测试

目标：
1. 验证 /api/stocks/collections/{name}/data 接口是否存在
2. 针对 6 个集合名称逐一检查
3. 无 Token 情况下至少返回 401 或 200；有 Token 时进一步验证结构

说明：
- 为了兼容当前环境，本测试在无 TEST_AUTH_TOKEN 时，只做接口存在性验证。
"""
import os
import httpx
import pytest


class TestStockCollectionDataApi:
    """股票数据集合数据接口测试类"""

    @pytest.fixture
    def api_base_url(self):
        return os.getenv("API_BASE_URL", "http://localhost:8000")

    @pytest.fixture
    def auth_headers(self):
        token = os.getenv("TEST_AUTH_TOKEN", "")
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    @pytest.fixture
    def collection_names(self):
        return [
            "stock_basic_info",
            "market_quotes",
            "stock_financial_data",
            "stock_daily",
            "stock_weekly",
            "stock_monthly",
        ]

    @pytest.mark.parametrize("collection_name", [
        "stock_basic_info",
        "market_quotes",
        "stock_financial_data",
        "stock_daily",
        "stock_weekly",
        "stock_monthly",
    ])
    def test_collection_data_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        """测试1：验证每个集合的数据接口是否存在"""
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"

        with httpx.Client(trust_env=False, timeout=5.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 5})

        assert response.status_code in [200, 401], \
            f"集合 {collection_name} 的数据接口应该存在（200或401），实际状态码: {response.status_code}"

    @pytest.mark.parametrize("collection_name", [
        "stock_basic_info",
        "market_quotes",
        "stock_financial_data",
        "stock_daily",
        "stock_weekly",
        "stock_monthly",
    ])
    def test_collection_data_structure_if_authorized(self, api_base_url, auth_headers, collection_name):
        """测试2：如果有token，则验证数据结构"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过结构验证")

        url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"
        with httpx.Client(trust_env=False, timeout=5.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 5})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data.get("success") is True
        assert "data" in data
        payload = data["data"]
        assert "items" in payload
        assert "total" in payload
        assert "page" in payload
        assert "page_size" in payload
        assert isinstance(payload["items"], list)

        # 如果有返回记录，至少检查 code 字段存在
        if payload["items"]:
            item = payload["items"][0]
            assert "code" in item
