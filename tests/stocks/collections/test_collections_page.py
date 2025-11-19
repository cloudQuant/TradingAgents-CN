"""
测试股票数据集合页面
测试目标：
1. 验证股票数据集合接口是否存在
2. 验证数据集合列表是否正确返回
3. 验证数据集合的字段定义是否完整
"""
import pytest
import httpx
import os


class TestStockCollectionsPage:
    """股票数据集合页面测试类"""
    
    @pytest.fixture
    def api_base_url(self):
        """API基础URL"""
        return os.getenv("API_BASE_URL", "http://localhost:8000")
    
    @pytest.fixture
    def auth_headers(self):
        """认证头部"""
        # TODO: 根据实际情况修改token获取方式
        token = os.getenv("TEST_AUTH_TOKEN", "")
        if token:
            return {"Authorization": f"Bearer {token}"}
        else:
            return {}  # 没有token时返回空字典，不发送Authorization头
    
    @pytest.fixture
    def expected_collections(self):
        """期望的股票数据集合名称"""
        return [
            'stock_basic_info',      # 1. 股票基础信息
            'market_quotes',          # 2. 实时行情数据
            'stock_financial_data',   # 3. 财务数据
            'stock_daily',            # 4. 日线行情
            'stock_weekly',           # 5. 周线行情
            'stock_monthly',          # 6. 月线行情
        ]
    
    def test_collections_endpoint_exists(self, api_base_url, auth_headers):
        """测试1：验证数据集合接口是否存在"""
        url = f"{api_base_url}/api/stocks/collections"
        
        # 使用独立的Client并禁用环境代理，避免访问localhost时走系统代理
        with httpx.Client(trust_env=False) as client:
            response = client.get(url, headers=auth_headers)
        
        assert response.status_code in [200, 401], \
            f"接口应该存在（200或401），实际状态码: {response.status_code}\n" \
            f"请在 app/routers/stocks.py 中添加 /collections 接口"
    
    def test_collections_list_structure(self, api_base_url, auth_headers):
        """测试2：验证数据集合列表结构是否正确"""
        url = f"{api_base_url}/api/stocks/collections"
        
        # 使用独立的Client并禁用环境代理
        with httpx.Client(trust_env=False) as client:
            response = client.get(url, headers=auth_headers)
        
        if response.status_code == 401:
            pytest.skip("需要认证，跳过此测试")
        
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list), "返回数据应该是列表"
        assert len(data) > 0, "数据集合列表不应该为空"
        
        # 验证每个集合的结构
        for collection in data:
            assert "name" in collection, "集合应该有 name 字段"
            assert "display_name" in collection, "集合应该有 display_name 字段"
            assert "description" in collection, "集合应该有 description 字段"
            assert "route" in collection, "集合应该有 route 字段"
            assert "fields" in collection, "集合应该有 fields 字段"
            assert isinstance(collection["fields"], list), "fields 应该是列表"
    
    def test_expected_collections_present(self, api_base_url, auth_headers, expected_collections):
        """测试3：验证期望的数据集合是否都存在"""
        url = f"{api_base_url}/api/stocks/collections"
        
        # 使用独立的Client并禁用环境代理
        with httpx.Client(trust_env=False) as client:
            response = client.get(url, headers=auth_headers)
        
        if response.status_code == 401:
            pytest.skip("需要认证，跳过此测试")
        
        assert response.status_code == 200
        
        data = response.json()
        collection_names = [c["name"] for c in data]
        
        for expected_name in expected_collections:
            assert expected_name in collection_names, \
                f"期望的集合 '{expected_name}' 未在返回数据中找到\n" \
                f"实际返回的集合: {collection_names}"
