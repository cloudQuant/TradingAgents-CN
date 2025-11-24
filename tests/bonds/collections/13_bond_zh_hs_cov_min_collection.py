"""可转债分时行情测试 - API: bond_zh_hs_cov_min - 集合: bond_zh_hs_cov_min - 唯一: 代码+时间+周期"""
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestBondZhHsCovMin:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_hs_cov_min")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert(self, collection):
        data = {"债券代码": "sz123124", "时间": "2021-09-06 09:35:00", "周期": "5", "开盘": 131.5, "收盘": 131.8, "成交量": 1500, "更新时间": datetime.now()}
        await collection.insert_one(data)
        found = await collection.find_one({"债券代码": "sz123124", "周期": "5"})
        assert found is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
