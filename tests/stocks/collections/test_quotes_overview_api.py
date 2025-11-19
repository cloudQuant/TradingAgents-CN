"""股票行情概览接口测试

目标：
1. 验证 /api/stocks/quotes/overview 接口是否存在
2. 在无 Token 情况下至少返回 401（需要认证）或 200（不需要认证）
3. 在有 Token 情况下（预留），验证数据结构

说明：
- 为了兼容当前环境，本测试在无 TEST_AUTH_TOKEN 时，只做接口存在性验证。
"""
import os
import httpx
import pytest


class TestStockQuotesOverviewApi:
    """股票行情概览接口测试类"""

    @pytest.fixture
    def api_base_url(self):
        return os.getenv("API_BASE_URL", "http://localhost:8000")

    @pytest.fixture
    def auth_headers(self):
        token = os.getenv("TEST_AUTH_TOKEN", "")
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    def test_overview_endpoint_exists(self, api_base_url, auth_headers):
        """测试1：验证行情概览接口是否存在"""
        url = f"{api_base_url}/api/stocks/quotes/overview"

        # 禁用系统代理，直接请求本地服务
        with httpx.Client(trust_env=False, timeout=5.0) as client:
            response = client.get(
                url,
                headers=auth_headers,
                params={"page": 1, "page_size": 20},
            )

        assert response.status_code in [200, 401], \
            f"接口应该存在（200或401），实际状态码: {response.status_code}"

    @pytest.mark.parametrize("sort_by", [
        "amount",
        "volume",
        "pct_chg",
        "close",
        "trade_date",
        "updated_at",
    ])
    def test_overview_sort_by_supported_fields(self, api_base_url, auth_headers, sort_by):
        """测试2：验证支持的排序字段不会导致接口报错

        无论是否提供 Token，只要接口存在且实现了排序参数处理，
        对允许的 sort_by 字段请求都不应返回 5xx 错误。
        """
        url = f"{api_base_url}/api/stocks/quotes/overview"
        with httpx.Client(trust_env=False, timeout=5.0) as client:
            response = client.get(
                url,
                headers=auth_headers,
                params={
                    "page": 1,
                    "page_size": 5,
                    "sort_by": sort_by,
                    "sort_dir": "desc",
                },
            )

        assert response.status_code in [200, 401], \
            f"sort_by={sort_by} 时接口应该存在（200或401），实际状态码: {response.status_code}"

    def test_overview_response_structure_if_authorized(self, api_base_url, auth_headers):
        """测试3：如果有token，则验证数据结构（包含分页字段）"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过结构验证")

        url = f"{api_base_url}/api/stocks/quotes/overview"
        with httpx.Client(trust_env=False, timeout=5.0) as client:
            response = client.get(
                url,
                headers=auth_headers,
                params={"page": 1, "page_size": 20},
            )

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

        if payload["items"]:
            item = payload["items"][0]
            # 只检查关键字段存在性，不强制类型
            for field in ["code", "name", "market", "latest_price", "pct_chg", "volume", "amount"]:
                assert field in item

    def test_overview_sort_result_if_authorized(self, api_base_url, auth_headers):
        """测试4：有 Token 时，简单验证按成交额降序排序结果"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过排序结果验证")

        url = f"{api_base_url}/api/stocks/quotes/overview"
        with httpx.Client(trust_env=False, timeout=5.0) as client:
            response = client.get(
                url,
                headers=auth_headers,
                params={
                    "page": 1,
                    "page_size": 10,
                    "sort_by": "amount",
                    "sort_dir": "desc",
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        payload = data.get("data", {})
        items = payload.get("items") or []

        # 如果数据量太少或没有有效的 amount 字段，则跳过排序验证
        if len(items) < 2:
            pytest.skip("返回记录不足，无法验证排序结果")

        amounts = [it.get("amount") for it in items if isinstance(it.get("amount"), (int, float))]
        if len(amounts) < 2:
            pytest.skip("有效 amount 字段不足，无法验证排序结果")

        # 验证列表是非严格降序（允许相等）
        assert all(amounts[i] >= amounts[i + 1] for i in range(len(amounts) - 1)), \
            "按成交额降序排序时，返回的数据顺序不符合预期"
