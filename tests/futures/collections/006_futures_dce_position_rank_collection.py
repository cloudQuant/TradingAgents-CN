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

class TestFuturesDcePositionRankCollection:
    """Test futures_dce_position_rank collection API"""

    def setup_method(self):
        self.collection_name = "futures_dce_position_rank"
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
                assert col["display_name"] == "大连商品交易所"
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
        # The structure of data here is a bit complex, it returns a dict of DataFrames in API, 
        # but in DB we probably store flattened records.
        # Let's assume we store flattened records with fields: date, symbol, rank, company, volume, etc.
        items = [
            {"_id": "1", "date": "20230101", "symbol": "m2305", "rank": 1, "member_name": "Company A", "vol": 1000},
            {"_id": "2", "date": "20230101", "symbol": "m2305", "rank": 2, "member_name": "Company B", "vol": 900}
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
        # ak.futures_dce_position_rank returns a dict of DataFrames
        mock_df = pd.DataFrame({
            "名次": [1, 2],
            "会员简称": ["Company A", "Company B"],
            "成交量": [1000, 900],
            "增减": [10, -10],
            "持买单量": [500, 400],
            "持买单量增减": [5, -5],
            "持卖单量": [600, 300],
            "持卖单量增减": [6, -6]
        })
        mock_ak.futures_dce_position_rank.return_value = {"m2305": mock_df}
        
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_update_one(*args, **kwargs):
            return MagicMock()
        mock_collection.update_one.side_effect = mock_update_one

        # The update for this one needs query param 'date'
        response = client.post(f"{self.base_url}/update?date=20230101")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["data"] or "task_id" in data["data"]
