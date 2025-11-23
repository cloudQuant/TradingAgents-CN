import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

sys.modules["akshare"] = MagicMock()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from app.main import app
from app.routers.auth_db import get_current_user

def mock_get_current_user():
    return {"username": "test_user", "id": "user_id"}

app.dependency_overrides[get_current_user] = mock_get_current_user
client = TestClient(app)

class TestFuturesHqSubscribeExchangeSymbolCollection:
    def setup_method(self):
        self.collection_name = "futures_hq_subscribe_exchange_symbol"
        self.base_url = f"/api/futures/collections/{self.collection_name}"

    def test_collection_info_exists(self):
        response = client.get("/api/futures/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        found = any(col["name"] == self.collection_name and col["display_name"] == "外盘-品种代码表" 
                   for col in data["data"])
        assert found is True

    @patch("app.routers.futures.get_mongo_db")
    def test_get_data(self, mock_get_db):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_count(*args, **kwargs):
            return 2
        mock_collection.count_documents.side_effect = mock_count
        
        mock_cursor = MagicMock()
        items = [
            {"_id": "1", "symbol": "COMEX黄金", "code": "GC"},
            {"_id": "2", "symbol": "NYMEX原油", "code": "CL"}
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
        mock_ak = sys.modules["akshare"]
        mock_df = pd.DataFrame({
            "symbol": ["COMEX黄金", "NYMEX原油"],
            "code": ["GC", "CL"]
        })
        mock_ak.futures_hq_subscribe_exchange_symbol.return_value = mock_df
        
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
