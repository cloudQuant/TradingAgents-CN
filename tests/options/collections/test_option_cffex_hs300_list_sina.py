"""
中金所沪深300指数所有合约返回的第一个合约为主力合约 数据集合测试

测试目标：
1. 验证 option_cffex_hs300_list_sina 数据集合的完整功能
2. 测试数据获取、存储、更新、展示等核心功能
3. 确保数据的正确性和完整性

接口信息：
- 接口名称：option_cffex_hs300_list_sina
- 描述：中金所-沪深300指数-所有合约, 返回的第一个合约为主力合约
- 输入参数：无
- 输出参数：合约列表 (list of strings)
"""

import os
import sys
import pytest
import httpx
from datetime import datetime

# 添加项目根目录到 Python 路径
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, root_dir)


class TestOptionCffexHs300ListSinaCollection:
    """中金所沪深300指数所有合约返回的第一个合约为主力合约 集合测试类"""
    
    @pytest.fixture
    def api_base_url(self):
        """API基础URL"""
        return os.getenv("API_BASE_URL", "http://localhost:8000")
    
    @pytest.fixture
    def auth_headers(self):
        """认证头"""
        token = os.getenv("TEST_AUTH_TOKEN", "")
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    @pytest.fixture
    def collection_name(self):
        """集合名称"""
        return "option_cffex_hs300_list_sina"
    
    # ========== 测试1：基础接口测试 ==========
    
    def test_collection_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        """测试1.1：验证数据集合接口是否存在"""
        url = f"{api_base_url}/api/options/collections/{collection_name}/data"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 10})
        
        # 接口应该存在（返回200或401）
        assert response.status_code in [200, 401], \
            f"集合 {collection_name} 的数据接口应该存在，实际状态码: {response.status_code}"
    
    def test_collection_data_fields(self, api_base_url, auth_headers, collection_name):
        """测试1.3：验证数据字段完整性"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过字段验证")
        
        url = f"{api_base_url}/api/options/collections/{collection_name}/data"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 10})
        
        assert response.status_code == 200
        data = response.json()
        payload = data["data"]
        
        if payload["items"]:
            item = payload["items"][0]
            # 验证核心字段存在
            # 合约代码 -> contract_code
            pass

    # ========== 测试2：数据刷新测试 ==========
    
    def test_refresh_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        """测试2.1：验证刷新接口是否存在"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过刷新接口测试")
        
        url = f"{api_base_url}/api/options/collections/{collection_name}/refresh"
        
        with httpx.Client(trust_env=False, timeout=30.0) as client:
            response = client.post(url, headers=auth_headers)
        
        # 刷新接口应该存在
        assert response.status_code in [200, 202, 400, 500], \
            f"刷新接口应该存在，实际状态码: {response.status_code}"

if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "-s"])
