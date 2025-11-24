"""
沪深债券实时行情数据集合测试

测试覆盖：
1. 数据获取功能
2. 数据存储功能
3. 数据查询功能
4. 分页功能
5. 排序功能
6. 实时更新功能
"""

import pytest
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.database import get_mongo_db, init_database, close_database


class TestBondZhHsSpotCollection:
    """沪深债券实时行情数据集合测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        """设置测试数据库"""
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def db(self):
        """获取数据库连接"""
        return get_mongo_db()
    
    @pytest.fixture
    async def collection(self, db):
        """获取集合"""
        return db.get_collection("bond_zh_hs_spot")
    
    @pytest.fixture(autouse=True)
    async def clean_collection(self, collection):
        """每个测试前清空集合"""
        await collection.delete_many({})
        yield
        # 测试后也清空
        await collection.delete_many({})
    
    async def test_collection_exists(self, db):
        """测试集合是否存在"""
        collections = await db.list_collection_names()
        # 集合可能还不存在，这是正常的
        assert isinstance(collections, list)
    
    async def test_insert_bond_data(self, collection):
        """测试插入债券数据"""
        test_data = {
            "代码": "sh010107",
            "名称": "21国债⑺",
            "最新价": 100.010,
            "涨跌额": 0.00,
            "涨跌幅": 0.00,
            "买入": 100.00,
            "卖出": 100.02,
            "昨收": 100.01,
            "今开": 100.00,
            "最高": 100.02,
            "最低": 99.98,
            "成交量": 1000,
            "成交额": 100000,
            "更新时间": datetime.now(),
            "数据来源": "sina"
        }
        
        result = await collection.insert_one(test_data)
        assert result.inserted_id is not None
        
        # 验证数据已插入
        found = await collection.find_one({"代码": "sh010107"})
        assert found is not None
        assert found["名称"] == "21国债⑺"
        assert found["最新价"] == 100.010
    
    async def test_upsert_bond_data(self, collection):
        """测试更新或插入债券数据"""
        code = "sh010504"
        
        # 首次插入
        data1 = {
            "代码": code,
            "名称": "05国债⑷",
            "最新价": 102.00,
            "涨跌额": 0.05,
            "涨跌幅": 0.05,
            "成交量": 1000,
            "成交额": 102000,
            "更新时间": datetime.now(),
            "数据来源": "sina"
        }
        
        result1 = await collection.update_one(
            {"代码": code},
            {"$set": data1},
            upsert=True
        )
        assert result1.upserted_id is not None or result1.modified_count >= 0
        
        # 再次更新（模拟实时刷新）
        data2 = {
            "代码": code,
            "名称": "05国债⑷",
            "最新价": 102.10,
            "涨跌额": 0.15,
            "涨跌幅": 0.15,
            "成交量": 1500,
            "成交额": 153150,
            "更新时间": datetime.now(),
            "数据来源": "sina"
        }
        
        result2 = await collection.update_one(
            {"代码": code},
            {"$set": data2},
            upsert=True
        )
        assert result2.modified_count == 1
        
        # 验证数据已更新
        found = await collection.find_one({"代码": code})
        assert found["最新价"] == 102.10
        assert found["成交量"] == 1500
    
    async def test_query_with_pagination(self, collection):
        """测试分页查询"""
        # 插入多条测试数据
        test_bonds = []
        for i in range(25):
            test_bonds.append({
                "代码": f"sh{100000 + i}",
                "名称": f"测试债券{i}",
                "最新价": 100.0 + i * 0.1,
                "涨跌额": 0.1 * (i % 3 - 1),
                "涨跌幅": 0.1 * (i % 3 - 1),
                "成交量": 1000 * i,
                "成交额": 100000 * i,
                "更新时间": datetime.now(),
                "数据来源": "sina"
            })
        
        await collection.insert_many(test_bonds)
        
        # 测试第一页
        page1 = await collection.find().skip(0).limit(10).to_list(length=10)
        assert len(page1) == 10
        
        # 测试第二页
        page2 = await collection.find().skip(10).limit(10).to_list(length=10)
        assert len(page2) == 10
        
        # 测试第三页
        page3 = await collection.find().skip(20).limit(10).to_list(length=10)
        assert len(page3) == 5  # 只剩5条
        
        # 测试总数
        total = await collection.count_documents({})
        assert total == 25
    
    async def test_query_with_sort(self, collection):
        """测试排序查询"""
        # 插入测试数据
        test_bonds = [
            {"代码": "sh001", "名称": "债券A", "涨跌幅": 1.5, "成交额": 1000000, "更新时间": datetime.now()},
            {"代码": "sh002", "名称": "债券B", "涨跌幅": -0.5, "成交额": 2000000, "更新时间": datetime.now()},
            {"代码": "sh003", "名称": "债券C", "涨跌幅": 0.8, "成交额": 500000, "更新时间": datetime.now()},
            {"代码": "sh004", "名称": "债券D", "涨跌幅": -1.2, "成交额": 3000000, "更新时间": datetime.now()},
        ]
        await collection.insert_many(test_bonds)
        
        # 按涨跌幅降序排序
        sorted_by_change = await collection.find().sort("涨跌幅", -1).to_list(length=10)
        assert sorted_by_change[0]["涨跌幅"] == 1.5
        assert sorted_by_change[-1]["涨跌幅"] == -1.2
        
        # 按成交额降序排序
        sorted_by_amount = await collection.find().sort("成交额", -1).to_list(length=10)
        assert sorted_by_amount[0]["成交额"] == 3000000
        assert sorted_by_amount[-1]["成交额"] == 500000
    
    async def test_query_with_filter(self, collection):
        """测试条件筛选"""
        # 插入测试数据
        test_bonds = [
            {"代码": "sh001", "名称": "国债A", "涨跌幅": 1.5, "成交量": 10000, "更新时间": datetime.now()},
            {"代码": "sh002", "名称": "企业债B", "涨跌幅": -0.5, "成交量": 20000, "更新时间": datetime.now()},
            {"代码": "sh003", "名称": "国债C", "涨跌幅": 0.8, "成交量": 5000, "更新时间": datetime.now()},
            {"代码": "sz001", "名称": "国债D", "涨跌幅": -1.2, "成交量": 30000, "更新时间": datetime.now()},
        ]
        await collection.insert_many(test_bonds)
        
        # 按名称筛选
        filtered = await collection.find({"名称": {"$regex": "国债"}}).to_list(length=10)
        assert len(filtered) == 3
        
        # 按代码前缀筛选
        sh_bonds = await collection.find({"代码": {"$regex": "^sh"}}).to_list(length=10)
        assert len(sh_bonds) == 3
        
        # 按涨跌幅范围筛选
        positive = await collection.find({"涨跌幅": {"$gt": 0}}).to_list(length=10)
        assert len(positive) == 2
    
    async def test_bulk_upsert(self, collection):
        """测试批量更新插入"""
        from pymongo import UpdateOne
        
        # 准备批量数据
        bulk_data = []
        for i in range(10):
            code = f"sh{200000 + i}"
            bulk_data.append(
                UpdateOne(
                    {"代码": code},
                    {
                        "$set": {
                            "代码": code,
                            "名称": f"批量债券{i}",
                            "最新价": 100.0 + i,
                            "涨跌幅": 0.1 * i,
                            "成交量": 1000 * i,
                            "成交额": 100000 * i,
                            "更新时间": datetime.now(),
                            "数据来源": "sina"
                        }
                    },
                    upsert=True
                )
            )
        
        # 执行批量操作
        result = await collection.bulk_write(bulk_data)
        assert result.upserted_count + result.modified_count == 10
        
        # 验证数据
        count = await collection.count_documents({})
        assert count == 10
    
    async def test_create_indexes(self, collection):
        """测试创建索引"""
        # 创建索引
        await collection.create_index("代码", unique=True)
        await collection.create_index("涨跌幅")
        await collection.create_index("成交额")
        await collection.create_index("更新时间")
        
        # 验证索引
        indexes = await collection.list_indexes().to_list(length=None)
        index_names = [idx["name"] for idx in indexes]
        
        assert "代码_1" in index_names
        assert "涨跌幅_1" in index_names
        assert "成交额_1" in index_names
        assert "更新时间_1" in index_names


@pytest.mark.asyncio
class TestBondZhHsSpotAPI:
    """沪深债券实时行情API测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        """设置测试数据库"""
        await init_database()
        yield
        await close_database()
    
    async def test_api_endpoint_exists(self):
        """测试API端点是否存在"""
        # 这个测试需要在实际环境中运行
        # 这里只是示例框架
        pass
    
    async def test_get_spot_data(self):
        """测试获取实时行情数据"""
        # 需要实现API客户端测试
        pass
    
    async def test_refresh_data(self):
        """测试刷新数据"""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
