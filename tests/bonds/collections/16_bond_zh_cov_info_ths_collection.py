"""可转债详情-同花顺测试 - API: bond_zh_cov_info_ths - 集合: bond_zh_cov_info_ths - 唯一: 债券代码"""
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestBondZhCovInfoThs:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_cov_info_ths")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert(self, collection):
        data = {"债券代码": "123247", "债券简称": "万凯转债", "正股代码": "371216", "正股简称": "万凯新材", "转股价格": 27.5, "更新时间": datetime.now(), "数据来源": "ths"}
        await collection.insert_one(data)
        found = await collection.find_one({"债券代码": "123247"})
        assert found["债券简称"] == "万凯转债"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
