import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Mock akshare before importing app to avoid ModuleNotFoundError
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

class TestFuturesFeesInfoCollection:
    """Test futures_fees_info collection API"""

    def setup_method(self):
        self.collection_name = "futures_fees_info"
        self.base_url = f"/api/futures/collections/{self.collection_name}"

    def test_collection_info_exists(self):
        """Test if the collection is listed in the collections list"""
        response = client.get("/api/futures/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        found = False
        for col in collections:
            if col["name"] == self.collection_name:
                found = True
                assert col["display_name"] == "期货交易费用参照表"
                break
        assert found is True, f"Collection {self.collection_name} not found in list"

    @patch("app.routers.futures.get_mongo_db")
    def test_get_data(self, mock_get_db):
        """Test getting data from the collection"""
        # Mock DB response
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        # Mock count_documents
        async def mock_count(*args, **kwargs):
            return 10
        mock_collection.count_documents.side_effect = mock_count
        
        # Mock find
        mock_cursor = MagicMock()
        items = [
            {"_id": "1", "exchange": "SHFE", "code": "cu", "name": "铜", "commission": 0.0001},
            {"_id": "2", "exchange": "SHFE", "code": "al", "name": "铝", "commission": 0.0002}
        ]
        mock_cursor.__aiter__.return_value = items
        mock_collection.find.return_value = mock_cursor
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor

        response = client.get(self.base_url)
        assert response.status_code == 200
        data = response.json()
        if not data["success"]:
            print(f"Error: {data.get('error')}")
        assert data["success"] is True
        assert len(data["data"]["items"]) == 2
        assert data["data"]["items"][0]["code"] == "cu"

    @patch("app.routers.futures.get_mongo_db")
    def test_update_data(self, mock_get_db):
        """Test updating data from remote source (akshare)"""
        # Configure global akshare mock
        mock_ak = sys.modules["akshare"]
        mock_df = pd.DataFrame({
            "交易所": ["SHFE", "DCE"],
            "合约代码": ["cu", "m"],
            "合约名称": ["铜", "豆粕"],
            "开仓费率（按金额）": [0.00005, 0.0001],
            "更新时间": ["2023-01-01", "2023-01-01"]
        })
        mock_ak.futures_fees_info.return_value = mock_df
        
        # Mock DB
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        # Mock update_one
        async def mock_update_one(*args, **kwargs):
            return MagicMock()
        mock_collection.update_one.side_effect = mock_update_one

        # Call update endpoint
        response = client.post(f"{self.base_url}/update")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["data"] or "task_id" in data["data"]
