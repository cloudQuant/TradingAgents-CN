import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os
import datetime

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

class TestFuturesRuleCollection:
    """Test futures_rule collection API"""

    def setup_method(self):
        self.collection_name = "futures_rule"
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
                assert col["display_name"] == "期货规则-交易日历表"
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
            {"_id": "1", "交易所": "SHFE", "品种": "铜", "代码": "cu2305"},
            {"_id": "2", "交易所": "DCE", "品种": "豆粕", "代码": "m2305"}
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
            "交易所": ["SHFE", "DCE"],
            "品种": ["铜", "豆粕"],
            "代码": ["cu2305", "m2305"],
            "交易保证金比例": [10.0, 8.0],
            "日期": ["20231205", "20231205"]
        })
        mock_ak.futures_rule.return_value = mock_df
        
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_update_one(*args, **kwargs):
            return MagicMock()
        mock_collection.update_one.side_effect = mock_update_one

        response = client.post(f"{self.base_url}/update")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["data"] or "task_id" in data["data"]
