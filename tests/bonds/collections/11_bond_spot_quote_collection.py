"""现券市场做市报价测试 - API: bond_spot_quote - 集合: bond_spot_quote - 唯一: 债券代码+日期"""
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestBondSpotQuote:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_spot_quote")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert(self, collection):
        data = {"债券代码": "101800018", "日期": "2023-01-03", "做市机构": "招商银行", "买入价": 100.5, "卖出价": 101.0, "更新时间": datetime.now()}
        await collection.insert_one(data)
        found = await collection.find_one({"债券代码": "101800018"})
        assert found is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
