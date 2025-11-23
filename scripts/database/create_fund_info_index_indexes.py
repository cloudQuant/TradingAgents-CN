#!/usr/bin/env python3
"""
为 fund_info_index_em 集合创建索引
使用 日期 + 基金代码 + 跟踪标的 作为唯一标识
"""
import asyncio
import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import init_database, close_database, get_mongo_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def create_indexes():
    """创建索引"""
    try:
        db = get_mongo_db()
        collection = db.get_collection('fund_info_index_em')
        
        logger.info("=" * 60)
        logger.info("开始为 fund_info_index_em 集合创建索引...")
        logger.info("=" * 60)
        
        # 1. 唯一复合索引：日期 + 基金代码 + 跟踪标的
        logger.info("创建唯一复合索引: 日期 + code + 跟踪标的")
        await collection.create_index(
            [
                ('日期', 1),
                ('code', 1),
                ('跟踪标的', 1)
            ],
            unique=True,
            name='idx_date_code_target_unique'
        )
        logger.info("✅ 唯一复合索引创建成功")
        
        # 2. 基金代码索引（用于按基金查询）
        logger.info("创建索引: code")
        await collection.create_index(
            [('code', 1)],
            name='idx_code'
        )
        logger.info("✅ code 索引创建成功")
        
        # 3. 日期索引（用于按日期查询和排序）
        logger.info("创建索引: 日期")
        await collection.create_index(
            [('日期', -1)],
            name='idx_date_desc'
        )
        logger.info("✅ 日期索引创建成功")
        
        # 4. 跟踪标的索引（用于按类型筛选）
        logger.info("创建索引: 跟踪标的")
        await collection.create_index(
            [('跟踪标的', 1)],
            name='idx_tracking_target'
        )
        logger.info("✅ 跟踪标的索引创建成功")
        
        # 5. 跟踪方式索引（用于按类型筛选）
        logger.info("创建索引: 跟踪方式")
        await collection.create_index(
            [('跟踪方式', 1)],
            name='idx_tracking_method'
        )
        logger.info("✅ 跟踪方式索引创建成功")
        
        # 6. 复合索引：跟踪标的 + 日期（常用查询组合）
        logger.info("创建复合索引: 跟踪标的 + 日期")
        await collection.create_index(
            [
                ('跟踪标的', 1),
                ('日期', -1)
            ],
            name='idx_target_date'
        )
        logger.info("✅ 跟踪标的+日期索引创建成功")
        
        # 列出所有索引
        logger.info("\n" + "=" * 60)
        logger.info("当前集合的所有索引:")
        logger.info("=" * 60)
        
        indexes = await collection.list_indexes().to_list(length=None)
        for idx in indexes:
            name = idx.get('name', 'unknown')
            keys = idx.get('key', {})
            unique = idx.get('unique', False)
            unique_str = " [UNIQUE]" if unique else ""
            logger.info(f"  - {name}: {dict(keys)}{unique_str}")
        
        logger.info("=" * 60)
        logger.info("索引创建完成！")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"创建索引失败: {e}", exc_info=True)
        raise


async def main():
    """主函数"""
    try:
        logger.info("初始化数据库连接...")
        await init_database()
        
        await create_indexes()
        
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
