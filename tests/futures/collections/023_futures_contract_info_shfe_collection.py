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

class TestFuturesContractInfoShfeCollection:
    """Test futures_contract_info_shfe collection API"""

    def setup_method(self):
        self.collection_name = "futures_contract_info_shfe"
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
                assert col["display_name"] == "上海期货交易所"
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
            {"_id": "1", "合约代码": "cu2401", "上市日": "20231015", "到期日": "20240115", "开始交割日": "20240116", "最后交割日": "20240119", "挂牌基准价": 65000.0, "交易日": "20240513", "更新时间": "2024-05-13 15:00:00"},
            {"_id": "2", "合约代码": "cu2402", "上市日": "20231115", "到期日": "20240215", "开始交割日": "20240216", "最后交割日": "20240219", "挂牌基准价": 65500.0, "交易日": "20240513", "更新时间": "2024-05-13 15:00:00"}
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
            "合约代码": ["cu2401", "cu2402"],
            "上市日": ["20231015", "20231115"],
            "到期日": ["20240115", "20240215"],
            "开始交割日": ["20240116", "20240216"],
            "最后交割日": ["20240119", "20240219"],
            "挂牌基准价": [65000.0, 65500.0],
            "交易日": ["20240513", "20240513"],
            "更新时间": ["2024-05-13 15:00:00", "2024-05-13 15:00:00"]
        })
        mock_ak.futures_contract_info_shfe.return_value = mock_df
        
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_update_one(*args, **kwargs):
            return MagicMock()
        mock_collection.update_one.side_effect = mock_update_one

        # This collection needs date parameter
        response = client.post(f"{self.base_url}/update?date=20240513")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["data"] or "task_id" in data["data"]
