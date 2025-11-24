"""
可转债数据一览表数据集合测试

API: bond_zh_cov
集合: bond_zh_cov
唯一标识: 债券代码
"""

import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database


class TestBondZhCovCollection:
    """可转债数据一览表测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_cov")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert_cov_data(self, collection):
        """测试插入可转债一览数据"""
        data = {
            "债券代码": "123240",
            "债券简称": "楚天转债",
            "申购日期": "2024-01-31",
            "申购代码": "370358",
            "申购上限": 10000.0,
            "正股代码": "003856",
            "正股简称": "楚天龙",
            "正股价": 28.5,
            "转股价": 27.5,
            "转股价值": 103.6,
            "债现价": 110.5,
            "转股溢价率": 6.7,
            "发行规模": 3.5,
            "中签率": 0.004307,
            "上市时间": "2024-02-29",
            "信用评级": "AA",
            "更新时间": datetime.now()
        }
        result = await collection.insert_one(data)
        assert result.inserted_id is not None
        
        found = await collection.find_one({"债券代码": "123240"})
        assert found["债券简称"] == "楚天转债"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
