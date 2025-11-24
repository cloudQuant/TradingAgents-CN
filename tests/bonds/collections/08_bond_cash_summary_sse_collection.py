"""
债券现券市场概览数据集合测试

API: bond_cash_summary_sse
集合: bond_cash_summary_sse
唯一标识: 债券类型 + 数据日期
"""

import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database


class TestBondCashSummarySSECollection:
    """债券现券市场概览测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_cash_summary_sse")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert_summary(self, collection):
        """测试插入市场概览数据"""
        data = {
            "债券类型": "国债",
            "数据日期": "2021-01-11",
            "托管只数": 193,
            "托管市值": 6815.47,  # 亿元
            "托管面值": 6758.46,  # 亿元
            "更新时间": datetime.now()
        }
        result = await collection.insert_one(data)
        assert result.inserted_id is not None
    
    async def test_composite_key(self, collection):
        """测试联合索引"""
        await collection.create_index([("债券类型", 1), ("数据日期", 1)], unique=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
