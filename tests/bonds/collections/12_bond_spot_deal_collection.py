"""现券市场成交行情测试 - API: bond_spot_deal - 集合: bond_spot_deal - 唯一: 债券代码+日期+时间"""
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestBondSpotDeal:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_spot_deal")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert(self, collection):
        data = {"债券代码": "101800018", "日期": "2023-01-03", "成交价": 100.8, "成交量": 1000.0, "成交额": 100800.0, "更新时间": datetime.now()}
        await collection.insert_one(data)
        assert await collection.count_documents({}) == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
