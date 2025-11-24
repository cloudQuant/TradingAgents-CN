"""可转债盘前分时测试 - API: bond_zh_hs_cov_pre_min - 集合: bond_zh_hs_cov_pre_min - 唯一: 代码+时间"""
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestBondZhHsCovPreMin:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_hs_cov_pre_min")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert(self, collection):
        data = {"债券代码": "sh113570", "时间": "2022-07-27 09:15:00", "开盘": 128.14, "收盘": 128.14, "最新价": 128.14, "更新时间": datetime.now()}
        await collection.insert_one(data)
        assert await collection.count_documents({"债券代码": "sh113570"}) == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
