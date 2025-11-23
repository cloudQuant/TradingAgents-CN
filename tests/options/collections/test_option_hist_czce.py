import os
import pytest
import requests

# 从环境变量获取配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8848")
AUTH_TOKEN = os.getenv("TEST_AUTH_TOKEN", "")

class TestOptionHistCzce:
    """测试郑州商品交易所商品期权集合"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """设置测试"""
        self.base_url = f"{API_BASE_URL}/options/collections/option_hist_czce"
        self.headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    def test_endpoint_exists(self):
        """测试端点是否存在"""
        response = requests.get(
            f"{self.base_url}/data",
            headers=self.headers,
            params={"page": 1, "page_size": 10}
        )
        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
    
    def test_refresh_endpoint(self):
        """测试刷新端点"""
        response = requests.post(
            f"{self.base_url}/refresh",
            headers=self.headers
        )
        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
    
    def test_stats_endpoint(self):
        """测试统计端点"""
        response = requests.get(
            f"{self.base_url}/stats",
            headers=self.headers
        )
        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert "success" in data
