import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Mock akshare before importing app
sys.modules["akshare"] = MagicMock()

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from app.main import app
from app.routers.auth_db import get_current_user

# Mock authentication
def mock_get_current_user():
    return {"username": "test_user", "id": "user_id"}

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

class TestFuturesContractInfoCffexCollection:
    """Test futures_contract_info_cffex collection API"""

    def setup_method(self):
        self.collection_name = "futures_contract_info_cffex"
        self.base_url = f"/api/futures/collections/{self.collection_name}"

    def test_collection_info_exists(self):
        """Test if the collection is listed"""
        response = client.get("/api/futures/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        found = False
        for col in collections:
            if col["name"] == self.collection_name:
                found = True
                assert col["display_name"] == "中国金融期货交易所"
                break
        assert found is True, f"Collection {self.collection_name} not found"

    @patch("app.routers.futures.get_mongo_db")
    def test_get_data(self, mock_get_db):
        """Test getting data"""
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_count(*args, **kwargs):
            return 5
        mock_collection.count_documents.side_effect = mock_count
        
        mock_cursor = MagicMock()
        items = [
            {"_id": "1", "合约代码": "IF2401", "合约月份": "202401", "挂盘基准价": 4000.0, "上市日": "20231015", "最后交易日": "20240115", "涨停板幅度": "10%", "跌停板幅度": "10%", "涨停板价位": 4400.0, "跌停板价位": 3600.0, "持仓限额": 1000, "品种": "沪深300股指", "查询交易日": "20240228"},
            {"_id": "2", "合约代码": "IF2402", "合约月份": "202402", "挂盘基准价": 4050.0, "上市日": "20231115", "最后交易日": "20240215", "涨停板幅度": "10%", "跌停板幅度": "10%", "涨停板价位": 4455.0, "跌停板价位": 3645.0, "持仓限额": 1000, "品种": "沪深300股指", "查询交易日": "20240228"}
        ]
        mock_cursor.__aiter__.return_value = items
        mock_collection.find.return_value = mock_cursor
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor

        response = client.get(self.base_url)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["items"]) == 2

    @patch("app.routers.futures.get_mongo_db")
    def test_update_data(self, mock_get_db):
        """Test update data"""
        mock_ak = sys.modules["akshare"]
        mock_df = pd.DataFrame({
            "合约代码": ["IF2401", "IF2402"],
            "合约月份": ["202401", "202402"],
            "挂盘基准价": [4000.0, 4050.0],
            "上市日": ["20231015", "20231115"],
            "最后交易日": ["20240115", "20240215"],
            "涨停板幅度": ["10%", "10%"],
            "跌停板幅度": ["10%", "10%"],
            "涨停板价位": [4400.0, 4455.0],
            "跌停板价位": [3600.0, 3645.0],
            "持仓限额": [1000, 1000],
            "品种": ["沪深300股指", "沪深300股指"],
            "查询交易日": ["20240228", "20240228"]
        })
        mock_ak.futures_contract_info_cffex.return_value = mock_df
        
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_update_one(*args, **kwargs):
            return MagicMock()
        mock_collection.update_one.side_effect = mock_update_one

        response = client.post(f"{self.base_url}/update?date=20240228")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["data"] or "task_id" in data["data"]
