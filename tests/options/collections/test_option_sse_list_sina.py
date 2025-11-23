"""
获取期权上交所50ETF合约到期月份列表 数据集合测试
"""

import os
import sys
import pytest
import httpx

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, root_dir)


class TestOptionSseListSinaCollection:
    """获取期权上交所50ETF合约到期月份列表 集合测试类"""
    
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
    def collection_name(self):
        return "option_sse_list_sina"
    
    def test_collection_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        url = f"{api_base_url}/api/options/collections/{collection_name}/data"
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 10})
        assert response.status_code in [200, 401]
    
    def test_refresh_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN")
        url = f"{api_base_url}/api/options/collections/{collection_name}/refresh"
        with httpx.Client(trust_env=False, timeout=30.0) as client:
            response = client.post(url, headers=auth_headers)
        assert response.status_code in [200, 202, 400, 500]

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
