"""
测试股票集合列表接口

测试目标：
1. 验证 GET /api/stocks/collections 接口返回所有已实现的集合
2. 确保集合信息（名称、显示名称、路由等）正确
"""

import os
import sys
import pytest
import httpx

# 添加项目根目录到 Python 路径
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, root_dir)


class TestStockCollectionsList:
    """股票集合列表测试类"""
    
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
    
    def test_list_collections(self, api_base_url, auth_headers):
        """测试获取集合列表"""
        if "Authorization" not in auth_headers:
            pytest.skip("未提供 TEST_AUTH_TOKEN，跳过测试")
            
        url = f"{api_base_url}/api/stocks/collections"
        
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            response = client.get(url, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list), "返回应该是列表"
        assert len(data) >= 14, "应该至少包含14个集合"
        
        # 期望存在的集合名称
        expected_collections = [
            "stock_basic_info",
            "market_quotes",
            "stock_financial_data",
            "stock_daily",
            "stock_weekly",
            "stock_monthly",
            "stock_sse_summary",            # 7
            "stock_szse_summary",           # 8
            "stock_szse_area_summary",      # 9
            "stock_szse_sector_summary",    # 10
            "stock_sse_deal_daily",         # 11
            "stock_individual_info_em",     # 12
            "stock_individual_basic_info_xq", # 13
            "stock_bid_ask_em",             # 14
        ]
        
        # 获取实际返回的集合名称
        actual_names = [item["name"] for item in data]
        
        # 验证所有期望的集合都存在
        for name in expected_collections:
            assert name in actual_names, f"集合 {name} 未在列表中返回"
            
        # 验证字段完整性
        for item in data:
            assert "name" in item
            assert "display_name" in item
            assert "description" in item
            assert "route" in item
            assert "fields" in item

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
