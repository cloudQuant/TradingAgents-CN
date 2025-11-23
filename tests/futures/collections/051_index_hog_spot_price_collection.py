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

class TestIndexHogSpotPriceCollection:
    def setup_method(self):
        self.collection_name = "index_hog_spot_price"
        self.base_url = f"/api/futures/collections/{self.collection_name}"

    def test_collection_info_exists(self):
        response = client.get("/api/futures/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        found = any(col["name"] == self.collection_name and col["display_name"] == "生猪市场价格指数" 
                   for col in data["data"])
        assert found is True

    @patch("app.routers.futures.get_mongo_db")
    def test_get_data(self, mock_get_db):
        mock_db, mock_collection = MagicMock(), MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        mock_collection.count_documents.side_effect = lambda *args, **kwargs: 2
        mock_cursor = MagicMock()
        items = [
            {"_id": "1", "日期": "2024-01-01", "指数": 120.5, "预售均价": 16.5, "成交均价": 16.3, "成交均重": 110},
            {"_id": "2", "日期": "2024-01-02", "指数": 121.0, "预售均价": 16.6, "成交均价": 16.4, "成交均重": 111}
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
        mock_df = pd.DataFrame({"日期": ["2024-01-01"], "指数": [120.5], "预售均价": [16.5]})
        mock_ak.index_hog_spot_price.return_value = mock_df
        mock_db, mock_collection = MagicMock(), MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        mock_collection.update_one.side_effect = lambda *args, **kwargs: MagicMock()
        response = client.post(f"{self.base_url}/update")
        assert response.status_code == 200
        assert response.json()["success"] is True
