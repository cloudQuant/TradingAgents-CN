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

class TestFuturesSettlementPriceSgxCollection:
    def setup_method(self):
        self.collection_name = "futures_settlement_price_sgx"
        self.base_url = f"/api/futures/collections/{self.collection_name}"

    def test_collection_info_exists(self):
        response = client.get("/api/futures/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        found = any(col["name"] == self.collection_name and col["display_name"] == "新加坡交易所期货" 
                   for col in data["data"])
        assert found is True

    @patch("app.routers.futures.get_mongo_db")
    def test_get_data(self, mock_get_db):
        mock_db, mock_collection = MagicMock(), MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_count(*args, **kwargs):
            return 2
        mock_collection.count_documents.side_effect = mock_count
        mock_cursor = MagicMock()
        items = [
            {"_id": "1", "DATE": 20231107, "COM": "NK", "COM_MM": 12, "COM_YY": 2023, "SETTLE": 33000.0},
            {"_id": "2", "DATE": 20231108, "COM": "NK", "COM_MM": 12, "COM_YY": 2023, "SETTLE": 33100.0}
        ]
        mock_cursor.__aiter__.return_value = items
        mock_collection.find.return_value = mock_cursor
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        response = client.get(self.base_url)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @patch("app.routers.futures.get_mongo_db")
    def test_update_data(self, mock_get_db):
        mock_ak = sys.modules["akshare"]
        mock_df = pd.DataFrame({"DATE": [20231107], "COM": ["NK"], "SETTLE": [33000.0]})
        mock_ak.futures_settlement_price_sgx.return_value = mock_df
        mock_db, mock_collection = MagicMock(), MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        mock_collection.update_one.side_effect = lambda *args, **kwargs: MagicMock()
        response = client.post(f"{self.base_url}/update?date=20231107")
        assert response.status_code == 200
        assert response.json()["success"] is True
