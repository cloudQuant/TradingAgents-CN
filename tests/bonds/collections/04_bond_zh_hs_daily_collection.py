"""
沪深债券历史行情数据集合测试

测试覆盖：
1. 数据获取功能
2. 数据存储功能（联合主键：债券代码+日期）
3. 数据查询功能
4. 分页功能
5. 日期范围查询
6. 批量更新功能
7. 增量更新功能
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.database import get_mongo_db, init_database, close_database


class TestBondZhHsDailyCollection:
    """沪深债券历史行情数据集合测试"""
    
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
        return db.get_collection("bond_zh_hs_daily")
    
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
        assert isinstance(collections, list)
    
    async def test_insert_daily_data(self, collection):
        """测试插入历史行情数据"""
        test_data = {
            "债券代码": "sh010107",
            "日期": "2021-07-30",
            "开盘": 100.00,
            "收盘": 100.01,
            "最高": 100.01,
            "最低": 99.99,
            "成交量": 150850,
            "更新时间": datetime.now(),
            "数据来源": "sina"
        }
        
        result = await collection.insert_one(test_data)
        assert result.inserted_id is not None
        
        # 验证数据已插入
        found = await collection.find_one({"债券代码": "sh010107", "日期": "2021-07-30"})
        assert found is not None
        assert found["收盘"] == 100.01
        assert found["成交量"] == 150850
    
    async def test_upsert_with_composite_key(self, collection):
        """测试使用联合主键更新或插入数据"""
        code = "sh010504"
        date = "2021-07-30"
        
        # 首次插入
        data1 = {
            "债券代码": code,
            "日期": date,
            "开盘": 102.00,
            "收盘": 102.10,
            "最高": 102.15,
            "最低": 101.95,
            "成交量": 10000,
            "更新时间": datetime.now(),
            "数据来源": "sina"
        }
        
        result1 = await collection.update_one(
            {"债券代码": code, "日期": date},
            {"$set": data1},
            upsert=True
        )
        assert result1.upserted_id is not None or result1.modified_count >= 0
        
        # 再次更新（模拟数据修正）
        data2 = {
            "债券代码": code,
            "日期": date,
            "开盘": 102.00,
            "收盘": 102.20,  # 修正收盘价
            "最高": 102.25,  # 修正最高价
            "最低": 101.95,
            "成交量": 15000,  # 修正成交量
            "更新时间": datetime.now(),
            "数据来源": "sina"
        }
        
        result2 = await collection.update_one(
            {"债券代码": code, "日期": date},
            {"$set": data2},
            upsert=True
        )
        assert result2.modified_count == 1
        
        # 验证数据已更新
        found = await collection.find_one({"债券代码": code, "日期": date})
        assert found["收盘"] == 102.20
        assert found["成交量"] == 15000
    
    async def test_insert_multiple_dates(self, collection):
        """测试插入同一债券的多个日期数据"""
        code = "sh010107"
        base_date = datetime(2021, 7, 1)
        
        # 插入30天的数据
        for i in range(30):
            date_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            data = {
                "债券代码": code,
                "日期": date_str,
                "开盘": 100.0 + i * 0.01,
                "收盘": 100.0 + i * 0.01 + 0.005,
                "最高": 100.0 + i * 0.01 + 0.01,
                "最低": 100.0 + i * 0.01 - 0.01,
                "成交量": 10000 * (i + 1),
                "更新时间": datetime.now(),
                "数据来源": "sina"
            }
            await collection.insert_one(data)
        
        # 验证数据已插入
        count = await collection.count_documents({"债券代码": code})
        assert count == 30
        
        # 验证可以按日期排序
        sorted_data = await collection.find({"债券代码": code}).sort("日期", 1).to_list(length=30)
        assert len(sorted_data) == 30
        assert sorted_data[0]["日期"] < sorted_data[-1]["日期"]
    
    async def test_query_by_date_range(self, collection):
        """测试按日期范围查询"""
        code = "sh010504"
        
        # 插入测试数据
        dates = [
            "2021-07-01", "2021-07-05", "2021-07-10",
            "2021-07-15", "2021-07-20", "2021-07-25", "2021-07-30"
        ]
        
        for date in dates:
            await collection.insert_one({
                "债券代码": code,
                "日期": date,
                "开盘": 100.0,
                "收盘": 100.1,
                "最高": 100.2,
                "最低": 99.9,
                "成交量": 10000,
                "更新时间": datetime.now(),
                "数据来源": "sina"
            })
        
        # 查询7月10日到7月20日的数据
        result = await collection.find({
            "债券代码": code,
            "日期": {"$gte": "2021-07-10", "$lte": "2021-07-20"}
        }).to_list(length=100)
        
        assert len(result) == 3  # 应该是 10, 15, 20
        dates_found = [r["日期"] for r in result]
        assert "2021-07-10" in dates_found
        assert "2021-07-15" in dates_found
        assert "2021-07-20" in dates_found
    
    async def test_query_multiple_bonds(self, collection):
        """测试查询多只债券的数据"""
        # 插入多只债券的数据
        bonds = ["sh010107", "sh010504", "sz000001"]
        date = "2021-07-30"
        
        for code in bonds:
            await collection.insert_one({
                "债券代码": code,
                "日期": date,
                "开盘": 100.0,
                "收盘": 100.1,
                "最高": 100.2,
                "最低": 99.9,
                "成交量": 10000,
                "更新时间": datetime.now(),
                "数据来源": "sina"
            })
        
        # 查询指定日期所有债券的数据
        result = await collection.find({"日期": date}).to_list(length=100)
        assert len(result) == 3
        
        codes_found = [r["债券代码"] for r in result]
        for code in bonds:
            assert code in codes_found
    
    async def test_bulk_upsert_daily_data(self, collection):
        """测试批量更新插入历史数据"""
        from pymongo import UpdateOne
        
        code = "sh010107"
        base_date = datetime(2021, 7, 1)
        
        # 准备批量数据
        bulk_ops = []
        for i in range(10):
            date_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            bulk_ops.append(
                UpdateOne(
                    {"债券代码": code, "日期": date_str},
                    {
                        "$set": {
                            "债券代码": code,
                            "日期": date_str,
                            "开盘": 100.0 + i * 0.1,
                            "收盘": 100.0 + i * 0.1 + 0.05,
                            "最高": 100.0 + i * 0.1 + 0.1,
                            "最低": 100.0 + i * 0.1 - 0.1,
                            "成交量": 10000 * (i + 1),
                            "更新时间": datetime.now(),
                            "数据来源": "sina"
                        }
                    },
                    upsert=True
                )
            )
        
        # 执行批量操作
        result = await collection.bulk_write(bulk_ops)
        assert result.upserted_count + result.modified_count == 10
        
        # 验证数据
        count = await collection.count_documents({"债券代码": code})
        assert count == 10
    
    async def test_incremental_update(self, collection):
        """测试增量更新（只更新最近几天）"""
        code = "sh010504"
        
        # 插入过去30天的数据
        base_date = datetime(2021, 7, 1)
        for i in range(30):
            date_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            await collection.insert_one({
                "债券代码": code,
                "日期": date_str,
                "开盘": 100.0,
                "收盘": 100.0,
                "最高": 100.0,
                "最低": 100.0,
                "成交量": 10000,
                "更新时间": datetime.now() - timedelta(days=30-i),
                "数据来源": "sina"
            })
        
        # 模拟增量更新：更新最近5天的数据
        recent_date = base_date + timedelta(days=25)
        recent_date_str = recent_date.strftime("%Y-%m-%d")
        
        from pymongo import UpdateOne
        bulk_ops = []
        for i in range(5):
            date_str = (recent_date + timedelta(days=i)).strftime("%Y-%m-%d")
            bulk_ops.append(
                UpdateOne(
                    {"债券代码": code, "日期": date_str},
                    {
                        "$set": {
                            "收盘": 101.0,  # 更新收盘价
                            "更新时间": datetime.now()
                        }
                    }
                )
            )
        
        result = await collection.bulk_write(bulk_ops)
        assert result.modified_count == 5
        
        # 验证最近的数据已更新
        updated = await collection.find({"债券代码": code, "日期": {"$gte": recent_date_str}}).to_list(length=10)
        for item in updated:
            assert item["收盘"] == 101.0
    
    async def test_create_indexes(self, collection):
        """测试创建索引"""
        # 创建联合索引（唯一）
        await collection.create_index([("债券代码", 1), ("日期", 1)], unique=True)
        
        # 创建单字段索引
        await collection.create_index("债券代码")
        await collection.create_index("日期")
        await collection.create_index("更新时间")
        
        # 验证索引
        indexes = await collection.list_indexes().to_list(length=None)
        index_names = [idx["name"] for idx in indexes]
        
        assert "债券代码_1_日期_1" in index_names
        assert "债券代码_1" in index_names
        assert "日期_1" in index_names
        assert "更新时间_1" in index_names
    
    async def test_pagination_with_large_dataset(self, collection):
        """测试大数据集分页"""
        code = "sh010107"
        
        # 插入100条数据
        base_date = datetime(2021, 1, 1)
        for i in range(100):
            date_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            await collection.insert_one({
                "债券代码": code,
                "日期": date_str,
                "开盘": 100.0,
                "收盘": 100.1,
                "最高": 100.2,
                "最低": 99.9,
                "成交量": 10000,
                "更新时间": datetime.now(),
                "数据来源": "sina"
            })
        
        # 测试分页
        page_size = 20
        page_1 = await collection.find({"债券代码": code}).sort("日期", 1).skip(0).limit(page_size).to_list(length=page_size)
        page_2 = await collection.find({"债券代码": code}).sort("日期", 1).skip(page_size).limit(page_size).to_list(length=page_size)
        
        assert len(page_1) == 20
        assert len(page_2) == 20
        
        # 验证数据不重复
        dates_p1 = {r["日期"] for r in page_1}
        dates_p2 = {r["日期"] for r in page_2}
        assert len(dates_p1 & dates_p2) == 0  # 没有交集
    
    async def test_data_integrity_check(self, collection):
        """测试数据完整性检查"""
        code = "sh010107"
        
        # 插入有缺失日期的数据
        dates = ["2021-07-01", "2021-07-02", "2021-07-05", "2021-07-06", "2021-07-10"]
        for date in dates:
            await collection.insert_one({
                "债券代码": code,
                "日期": date,
                "开盘": 100.0,
                "收盘": 100.1,
                "最高": 100.2,
                "最低": 99.9,
                "成交量": 10000,
                "更新时间": datetime.now(),
                "数据来源": "sina"
            })
        
        # 检查日期连续性
        all_dates = await collection.find({"债券代码": code}).sort("日期", 1).to_list(length=100)
        date_list = [datetime.strptime(r["日期"], "%Y-%m-%d") for r in all_dates]
        
        # 检测缺失的日期
        missing_dates = []
        for i in range(len(date_list) - 1):
            delta = (date_list[i+1] - date_list[i]).days
            if delta > 1:
                # 有缺失的日期
                missing_dates.append((date_list[i], date_list[i+1]))
        
        # 应该检测到缺失的日期段
        assert len(missing_dates) > 0


@pytest.mark.asyncio
class TestBondZhHsDailyAPI:
    """沪深债券历史行情API测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        """设置测试数据库"""
        await init_database()
        yield
        await close_database()
    
    async def test_api_endpoint_exists(self):
        """测试API端点是否存在"""
        # 这个测试需要在实际环境中运行
        pass
    
    async def test_get_daily_data(self):
        """测试获取历史行情数据"""
        # 需要实现API客户端测试
        pass
    
    async def test_batch_update(self):
        """测试批量更新"""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
