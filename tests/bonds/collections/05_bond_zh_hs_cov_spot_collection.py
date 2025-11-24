"""
可转债实时行情数据集合测试

API: bond_zh_hs_cov_spot
集合: bond_zh_hs_cov_spot
唯一标识: 代码
"""

import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database


class TestBondZhHsCovSpotCollection:
    """可转债实时行情测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_zh_hs_cov_spot")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert_convertible_bond(self, collection):
        """测试插入可转债数据"""
        data = {
            "代码": "123001",
            "转债名称": "蓝思转债",
            "现价": 131.5,
            "涨跌幅": 2.5,
            "正股代码": "300433",
            "正股名称": "蓝思科技",
            "正股价": 25.8,
            "正股涨跌": 3.2,
            "转股价": 19.5,
            "转股价值": 132.3,
            "转股溢价率": -0.6,
            "成交额": 15000000,
            "换手率": 8.5,
            "更新时间": datetime.now()
        }
        result = await collection.insert_one(data)
        assert result.inserted_id is not None
        
        found = await collection.find_one({"代码": "123001"})
        assert found["转债名称"] == "蓝思转债"
        assert found["转股溢价率"] == -0.6
    
    async def test_create_indexes(self, collection):
        """测试索引"""
        await collection.create_index("代码", unique=True)
        await collection.create_index("转股溢价率")
        await collection.create_index("涨跌幅")
        
        indexes = await collection.list_indexes().to_list(None)
        index_names = [idx["name"] for idx in indexes]
        assert "代码_1" in index_names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
