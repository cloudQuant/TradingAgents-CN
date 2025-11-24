"""
债券成交概览数据集合测试

API: bond_deal_summary_sse
集合: bond_deal_summary_sse
唯一标识: 债券类型 + 数据日期
"""

import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database


class TestBondDealSummarySSECollection:
    """债券成交概览测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_deal_summary_sse")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert_deal_summary(self, collection):
        """测试插入成交概览数据"""
        data = {
            "债券类型": "记账式国债",
            "数据日期": "2021-01-04",
            "当日成交笔数": 3685,
            "当日成交金额": 363349.44,  # 万元
            "当年成交笔数": 3685,
            "当年成交金额": 363349.44,  # 万元
            "更新时间": datetime.now()
        }
        result = await collection.insert_one(data)
        assert result.inserted_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
