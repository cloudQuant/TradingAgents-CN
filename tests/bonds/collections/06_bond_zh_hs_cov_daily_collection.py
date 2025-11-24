"""
可转债历史行情数据集合测试

API: bond_zh_hs_cov_daily
集合: bond_zh_hs_cov_daily
唯一标识: 债券代码 + 日期
"""

import pytest
from datetime import datetime, timedelta
from app.core.database import get_mongo_db, init_database, close_database


class TestBondZhHsCovDailyCollection:
    """可转债历史行情测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_hs_cov_daily")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert_daily_data(self, collection):
        """测试插入可转债历史数据"""
        data = {
            "债券代码": "sz128039",
            "日期": "2024-02-28",
            "开盘": 105.00,
            "收盘": 105.98,
            "最高": 106.50,
            "最低": 104.80,
            "成交量": 149757,
            "更新时间": datetime.now()
        }
        result = await collection.insert_one(data)
        assert result.inserted_id is not None
    
    async def test_composite_key_index(self, collection):
        """测试联合索引"""
        await collection.create_index([("债券代码", 1), ("日期", 1)], unique=True)
        
        indexes = await collection.list_indexes().to_list(None)
        index_names = [idx["name"] for idx in indexes]
        assert "债券代码_1_日期_1" in index_names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
