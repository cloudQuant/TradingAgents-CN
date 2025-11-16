"""
测试债券API路由
包括：可转债比价、价值分析等API接口的测试
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, AsyncMock
import pandas as pd


# 测试可转债比价表API
def test_get_convertible_comparison_api():
    """测试获取可转债比价表API"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock数据库和服务
    with patch('app.routers.bonds.get_mongo_db') as mock_get_db:
        with patch('app.routers.bonds.BondDataService') as mock_service_class:
            # 创建mock service实例
            mock_service = Mock()
            mock_service.query_cov_comparison = AsyncMock(return_value={
                "total": 2,
                "items": [
                    {
                        "code": "113682",
                        "name": "益丰转债",
                        "price": 120.5,
                        "convert_premium_rate": 12.0
                    },
                    {
                        "code": "127105",
                        "name": "龙星转债",
                        "price": 145.7,
                        "convert_premium_rate": 23.4
                    }
                ]
            })
            mock_service_class.return_value = mock_service
            mock_get_db.return_value = Mock()
            
            # Mock认证
            with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
                # 发送请求
                response = client.get(
                    "/api/bonds/convertible/comparison",
                    params={
                        "page": 1,
                        "page_size": 50,
                        "sort_by": "convert_premium_rate",
                        "sort_dir": "asc"
                    }
                )
                
                # 验证
                assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
                data = response.json()
                assert data["success"] is True
                assert data["data"]["total"] == 2
                assert len(data["data"]["items"]) == 2
                assert data["data"]["items"][0]["code"] == "113682"
    
    print("✅ 测试通过：获取可转债比价表API")


def test_sync_convertible_comparison_api():
    """测试同步可转债比价数据API"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock AKShare Provider
    with patch('app.routers.bonds.AKShareBondProvider') as mock_provider_class:
        # 创建mock provider
        mock_provider = Mock()
        mock_df = pd.DataFrame([
            {"转债代码": "113682", "转债名称": "益丰转债"}
        ])
        mock_provider.get_cov_comparison = AsyncMock(return_value=mock_df)
        mock_provider_class.return_value = mock_provider
        
        # Mock数据库和服务
        with patch('app.routers.bonds.get_mongo_db') as mock_get_db:
            with patch('app.routers.bonds.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.save_cov_comparison = AsyncMock(return_value=1)
                mock_service_class.return_value = mock_service
                mock_get_db.return_value = Mock()
                
                # Mock认证
                with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
                    # 发送POST请求
                    response = client.post("/api/bonds/convertible/comparison/sync")
                    
                    # 验证
                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["data"]["saved"] == 1
                    assert "message" in data["data"]
    
    print("✅ 测试通过：同步可转债比价数据API")


def test_get_value_analysis_api():
    """测试获取可转债价值分析API"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock数据库和服务
    with patch('app.routers.bonds.get_mongo_db') as mock_get_db:
        with patch('app.routers.bonds.BondDataService') as mock_service_class:
            mock_service = Mock()
            mock_service.query_cov_value_analysis = AsyncMock(return_value={
                "code": "113682",
                "data": [
                    {
                        "date": "2024-01-01",
                        "close_price": 120.0,
                        "convert_premium_rate": 9.1
                    }
                ]
            })
            mock_service_class.return_value = mock_service
            mock_get_db.return_value = Mock()
            
            # Mock认证
            with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
                # 发送请求
                response = client.get(
                    "/api/bonds/convertible/113682/value-analysis",
                    params={
                        "start_date": "2024-01-01",
                        "end_date": "2024-01-31"
                    }
                )
                
                # 验证
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "code" in data["data"]
                assert "data" in data["data"]
                assert len(data["data"]["data"]) == 1
    
    print("✅ 测试通过：获取可转债价值分析API")


def test_sync_value_analysis_api():
    """测试同步价值分析数据API"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock AKShare Provider
    with patch('app.routers.bonds.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_df = pd.DataFrame([
            {"日期": "2024-01-01", "收盘价": 120.0}
        ])
        mock_provider.get_cov_value_analysis = AsyncMock(return_value=mock_df)
        mock_provider_class.return_value = mock_provider
        
        # Mock数据库和服务
        with patch('app.routers.bonds.get_mongo_db') as mock_get_db:
            with patch('app.routers.bonds.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.save_cov_value_analysis = AsyncMock(return_value=1)
                mock_service_class.return_value = mock_service
                mock_get_db.return_value = Mock()
                
                # Mock认证
                with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
                    # 发送POST请求
                    response = client.post("/api/bonds/convertible/113682/value-analysis/sync")
                    
                    # 验证
                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert data["data"]["saved"] == 1
    
    print("✅ 测试通过：同步价值分析数据API")


def test_get_spot_deals_api():
    """测试获取现券市场成交行情API"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock AKShare Provider
    with patch('app.routers.bonds.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_df = pd.DataFrame([
            {
                "债券简称": "23附息国债26",
                "成交净价": 103.20,
                "最新收益率": 2.30
            }
        ])
        mock_provider.get_spot_deal = AsyncMock(return_value=mock_df)
        mock_provider_class.return_value = mock_provider
        
        # Mock认证
        with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
            # 发送请求
            response = client.get("/api/bonds/market/spot-deals")
            
            # 验证
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "items" in data["data"]
            assert len(data["data"]["items"]) == 1
    
    print("✅ 测试通过：获取现券市场成交行情API")


def test_get_spot_quotes_api():
    """测试获取现券市场做市报价API"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock AKShare Provider
    with patch('app.routers.bonds.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_df = pd.DataFrame([
            {
                "报价机构": "星展银行(中国)",
                "债券简称": "21进出10",
                "买入净价": 100.34,
                "卖出净价": 102.44
            }
        ])
        mock_provider.get_spot_quote = AsyncMock(return_value=mock_df)
        mock_provider_class.return_value = mock_provider
        
        # Mock认证
        with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
            # 发送请求
            response = client.get("/api/bonds/market/spot-quotes")
            
            # 验证
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "items" in data["data"]
            assert len(data["data"]["items"]) == 1
    
    print("✅ 测试通过：获取现券市场做市报价API")


def test_api_error_handling():
    """测试API错误处理"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock数据库返回None（模拟连接失败）
    with patch('app.routers.bonds.get_mongo_db', return_value=None):
        # Mock认证
        with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
            # 发送请求
            response = client.get("/api/bonds/convertible/comparison")
            
            # 验证错误处理
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
    
    print("✅ 测试通过：API错误处理")


def test_api_pagination():
    """测试API分页功能"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock数据库和服务
    with patch('app.routers.bonds.get_mongo_db') as mock_get_db:
        with patch('app.routers.bonds.BondDataService') as mock_service_class:
            mock_service = Mock()
            # 返回第2页的数据
            mock_service.query_cov_comparison = AsyncMock(return_value={
                "total": 100,
                "items": [{"code": f"11368{i}"} for i in range(2, 12)]  # 第2页10条数据
            })
            mock_service_class.return_value = mock_service
            mock_get_db.return_value = Mock()
            
            # Mock认证
            with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
                # 请求第2页，每页10条
                response = client.get(
                    "/api/bonds/convertible/comparison",
                    params={"page": 2, "page_size": 10}
                )
                
                # 验证
                assert response.status_code == 200
                data = response.json()
                assert data["data"]["page"] == 2
                assert data["data"]["page_size"] == 10
                assert data["data"]["total"] == 100
    
    print("✅ 测试通过：API分页功能")


def test_api_filtering():
    """测试API过滤功能"""
    from app.main import app
    
    client = TestClient(app)
    
    # Mock数据库和服务
    with patch('app.routers.bonds.get_mongo_db') as mock_get_db:
        with patch('app.routers.bonds.BondDataService') as mock_service_class:
            mock_service = Mock()
            # 返回满足溢价率条件的数据
            mock_service.query_cov_comparison = AsyncMock(return_value={
                "total": 10,
                "items": [
                    {"code": "113682", "convert_premium_rate": 5.0},
                    {"code": "127105", "convert_premium_rate": 8.0}
                ]
            })
            mock_service_class.return_value = mock_service
            mock_get_db.return_value = Mock()
            
            # Mock认证
            with patch('app.routers.bonds.get_current_user', return_value={"username": "test"}):
                # 请求溢价率在0-10%之间的数据
                response = client.get(
                    "/api/bonds/convertible/comparison",
                    params={"min_premium": 0, "max_premium": 10}
                )
                
                # 验证
                assert response.status_code == 200
                data = response.json()
                # 所有返回的数据溢价率应在0-10之间
                for item in data["data"]["items"]:
                    assert 0 <= item["convert_premium_rate"] <= 10
    
    print("✅ 测试通过：API过滤功能")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
