"""
交易排行榜-数据集合测试

测试目标：
1. 验证 stock_hot_deal_xq 数据集合的完整功能
2. 测试数据获取、存储、更新、展示等核心功能
3. 确保数据的正确性和完整性

接口信息：
- 接口名称：stock_hot_deal_xq
- 描述：雪球-沪深股市-热度排行榜-交易排行榜
- 输入参数：symbol (默认 "最热门")
- 输出参数：股票代码, 股票简称, 关注, 最新价
"""

import os
import sys
import pytest
import httpx
from datetime import datetime

# 添加项目根目录到 Python 路径
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, root_dir)


class TestStockHotDealXqCollection:
    """交易排行榜 集合测试类"""
    
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
        return "stock_hot_deal_xq"
    
    # ========== 测试1：基础接口测试 ==========
    
    def test_collection_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        """测试1.1：验证数据集合接口是否存在"""
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 10})
        
        # 接口应该存在（返回200或401）
        assert response.status_code in [200, 401], \
            f"集合 {collection_name} 的数据接口应该存在，实际状态码: {response.status_code}"
    
    def test_collection_data_structure(self, api_base_url, auth_headers, collection_name):
        """测试1.2：验证返回数据结构"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过数据结构验证")
        
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 10})
        
        assert response.status_code == 200, f"请求失败: {response.status_code}"
        
        data = response.json()
        assert isinstance(data, dict), "返回数据应该是字典"
        assert data.get("success") is True, "success 字段应该为 True"
        assert "data" in data, "应该包含 data 字段"
        
        payload = data["data"]
        assert "items" in payload, "应该包含 items 字段"
        assert "total" in payload, "应该包含 total 字段"
        assert "page" in payload, "应该包含 page 字段"
        assert "page_size" in payload, "应该包含 page_size 字段"
        assert isinstance(payload["items"], list), "items 应该是列表"
    
    def test_collection_data_fields(self, api_base_url, auth_headers, collection_name):
        """测试1.3：验证数据字段完整性"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过字段验证")
        
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 10})
        
        assert response.status_code == 200
        data = response.json()
        payload = data["data"]
        
        if payload["items"]:
            item = payload["items"][0]
            # 验证核心字段存在
            assert "股票代码" in item or "code" in item, "应该包含股票代码字段"
            assert "股票简称" in item or "name" in item, "应该包含股票简称字段"
            assert "关注" in item or "follow" in item, "应该包含关注字段"
            assert "最新价" in item or "price" in item, "应该包含最新价字段"
    
    # ========== 测试2：数据刷新测试 ==========
    
    def test_refresh_endpoint_exists(self, api_base_url, auth_headers, collection_name):
        """测试2.1：验证刷新接口是否存在"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过刷新接口测试")
        
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/refresh"
        
        with httpx.Client(trust_env=False, timeout=30.0) as client:
            response = client.post(url, headers=auth_headers, json={})
        
        # 刷新接口应该存在
        assert response.status_code in [200, 202, 400, 500], \
            f"刷新接口应该存在，实际状态码: {response.status_code}"
    
    def test_refresh_creates_data(self, api_base_url, auth_headers, collection_name):
        """测试2.2：验证刷新功能能够创建数据"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过刷新功能测试")
        
        # 1. 执行刷新
        refresh_url = f"{api_base_url}/api/stocks/collections/{collection_name}/refresh"
        
        # 使用示例代码
        params = {"symbol": "最热门"}
        
        with httpx.Client(trust_env=False, timeout=60.0) as client:
            refresh_response = client.post(refresh_url, headers=auth_headers, json=params)
        
        # 刷新可能是异步的，检查返回
        if refresh_response.status_code in [200, 202]:
            # 2. 等待一段时间后查询数据
            import time
            time.sleep(5)  # 等待5秒
            
            # 3. 验证数据已创建
            data_url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"
            
            with httpx.Client(trust_env=False, timeout=10.0) as client:
                data_response = client.get(data_url, headers=auth_headers, params={"page": 1, "page_size": 10})
            
            assert data_response.status_code == 200
            data = data_response.json()
            
            # 验证有数据返回
            assert "items" in data["data"], "应该返回items列表"
    
    # ========== 测试3：数据概览测试 ==========
    
    def test_collection_overview(self, api_base_url, auth_headers, collection_name):
        """测试3.1：验证数据概览功能"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过概览测试")
        
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/overview"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict), "概览数据应该是字典"
            # 概览应该包含统计信息
            assert "total" in data or "count" in data, "概览应该包含总数信息"
    
    # ========== 测试4：分页测试 ==========
    
    def test_pagination(self, api_base_url, auth_headers, collection_name):
        """测试4.1：验证分页功能"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过分页测试")
        
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/data"
        
        # 测试第1页
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response1 = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 5})
        
        assert response1.status_code == 200
        data1 = response1.json()
        
        # 如果有足够的数据，测试第2页
        if data1["data"]["total"] > 5:
            with httpx.Client(trust_env=False, timeout=10.0) as client:
                response2 = client.get(url, headers=auth_headers, params={"page": 2, "page_size": 5})
            
            assert response2.status_code == 200
            data2 = response2.json()
            
            # 两页数据不应该相同
            if data1["data"]["items"] and data2["data"]["items"]:
                assert data1["data"]["items"][0] != data2["data"]["items"][0], "不同页面应该返回不同数据"
    
    # ========== 测试5：清空数据测试 ==========
    
    def test_clear_data(self, api_base_url, auth_headers, collection_name):
        """测试5.1：验证清空数据功能"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过清空测试")
        
        url = f"{api_base_url}/api/stocks/collections/{collection_name}/clear"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.post(url, headers=auth_headers)
        
        # 清空接口应该存在
        if response.status_code not in [404]:
            assert response.status_code in [200, 202, 204], \
                f"清空接口调用失败: {response.status_code}"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "-s"])
