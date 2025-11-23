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

class TestFuturesHistEmCollection:
    """Test futures_hist_em collection API"""

    def setup_method(self):
        self.collection_name = "futures_hist_em"
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
                assert col["display_name"] == "内盘-历史行情数据-东财"
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
            {"_id": "1", "时间": "2024-01-01", "开盘": 3500, "最高": 3550, "最低": 3480, "收盘": 3520, "涨跌": 20, "涨跌幅": 0.57, "成交量": 120000, "成交额": 420000, "持仓量": 80000},
            {"_id": "2", "时间": "2024-01-02", "开盘": 3520, "最高": 3570, "最低": 3500, "收盘": 3550, "涨跌": 30, "涨跌幅": 0.85, "成交量": 130000, "成交额": 457000, "持仓量": 82000}
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
            "时间": ["2024-01-01", "2024-01-02"],
            "开盘": [3500, 3520],
            "最高": [3550, 3570],
            "最低": [3480, 3500],
            "收盘": [3520, 3550],
            "涨跌": [20, 30],
            "涨跌幅": [0.57, 0.85],
            "成交量": [120000, 130000],
            "成交额": [420000, 457000],
            "持仓量": [80000, 82000]
        })
        mock_ak.futures_hist_em.return_value = mock_df
        
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        
        async def mock_update_one(*args, **kwargs):
            return MagicMock()
        mock_collection.update_one.side_effect = mock_update_one

        response = client.post(f"{self.base_url}/update?symbol=热卷主连&period=daily&start_date=19900101&end_date=20500101")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "updated" in data["data"] or "task_id" in data["data"]
