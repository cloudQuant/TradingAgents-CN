"""
pytest配置文件 - 为所有集合测试提供fixture
"""
import sys
import os
import pytest
import asyncio
import pytest_asyncio

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.database import init_database, close_database, db_manager
from app.services.bond_data_service import BondDataService


@pytest_asyncio.fixture
async def database():
    """初始化数据库连接（每个测试独立）"""
    # 初始化MongoDB
    await init_database()
    
    # 获取数据库实例
    db = db_manager.mongo_db
    
    yield db
    
    # 清理
    await close_database()


@pytest_asyncio.fixture
async def bond_service(database):
    """创建债券数据服务实例"""
    service = BondDataService(database)
    return service


@pytest.fixture
def test_bond_code():
    """测试用的债券代码 - 使用活跃的可转债"""
    return "sh110062"  # 鹏辞转债 (有历史数据)

@pytest.fixture
def test_bond_codes():
    """多个测试债券代码 - 都是活跃可转债"""
    return [
        "sh110062",  # 鹏辞转债
        "sh110063",  # 鹰19转债
        "sh110064",  # 凯龙转债
        "110062",  # 不带前缀
    ]
