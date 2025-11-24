"""可转债详情-东财测试 - API: bond_zh_cov_info - 集合: bond_zh_cov_info - 唯一: 代码+指标类型"""
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestBondZhCovInfo:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_cov_info")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert(self, collection):
        data = {"债券代码": "123121", "指标类型": "基本信息", "详情数据": {"SECURITY_CODE": "123121", "转股价": 19.5}, "更新时间": datetime.now()}
        await collection.insert_one(data)
        found = await collection.find_one({"债券代码": "123121", "指标类型": "基本信息"})
        assert found["详情数据"]["SECURITY_CODE"] == "123121"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
