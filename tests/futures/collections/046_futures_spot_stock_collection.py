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

class TestFuturesSpotStockCollection:
    def setup_method(self):
        self.collection_name = "futures_spot_stock"
        self.base_url = f"/api/futures/collections/{self.collection_name}"

    def test_collection_info_exists(self):
        response = client.get("/api/futures/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        found = any(col["name"] == self.collection_name and col["display_name"] == "现货与股票" 
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
            {"_id": "1", "商品名称": "原油", "最新价": 520.0, "近半年涨跌幅": 10.5},
            {"_id": "2", "商品名称": "天然气", "最新价": 4.5, "近半年涨跌幅": -5.2}
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
        mock_df = pd.DataFrame({"商品名称": ["原油"], "最新价": [520.0], "近半年涨跌幅": [10.5]})
        mock_ak.futures_spot_stock.return_value = mock_df
        mock_db, mock_collection = MagicMock(), MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        mock_collection.update_one.side_effect = lambda *args, **kwargs: MagicMock()
        response = client.post(f"{self.base_url}/update?symbol=能源")
        assert response.status_code == 200
        assert response.json()["success"] is True
