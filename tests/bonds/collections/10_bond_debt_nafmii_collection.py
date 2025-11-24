"""
银行间市场债券发行数据集合测试

API: bond_debt_nafmii
集合: bond_debt_nafmii
唯一标识: 债券名称 + 注册通知书文号
"""

import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database


class TestBondDebtNafmiiCollection:
    """银行间市场债券发行测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("bond_debt_nafmii")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_insert_nafmii_data(self, collection):
        """测试插入银行间债券发行数据"""
        data = {
            "债券名称": "江苏黄海金融控股集团有限公司关于2024年度第一期中期票据的注册报告",
            "品种": "MTN",
            "注册或备案": "注册",
            "金额": 5.0,  # 亿元
            "注册通知书文号": "中市协注[2024]MTN123号",
            "更新日期": "2024-03-15",
            "项目状态": "40",
            "更新时间": datetime.now()
        }
        result = await collection.insert_one(data)
        assert result.inserted_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
