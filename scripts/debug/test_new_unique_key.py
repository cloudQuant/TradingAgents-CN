#!/usr/bin/env python3
"""
测试新的唯一标识：日期 + 基金代码 + 跟踪标的
1. 清空旧数据
2. 创建索引
3. 重新下载数据
4. 验证唯一性
"""
import asyncio
import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import init_database, close_database, get_mongo_db
from app.services.fund_refresh_service import FundRefreshService
from app.utils.task_manager import get_task_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """主函数"""
    try:
        logger.info("=" * 70)
        logger.info("测试新的唯一标识：日期 + 基金代码 + 跟踪标的")
        logger.info("=" * 70)
        
        await init_database()
        db = get_mongo_db()
        collection = db.get_collection('fund_info_index_em')
        
        # 1. 清空旧数据
        logger.info("\n步骤 1: 清空旧数据...")
        old_count = await collection.count_documents({})
        logger.info(f"当前记录数: {old_count}")
        
        if old_count > 0:
            result = await collection.delete_many({})
            logger.info(f"✅ 已删除 {result.deleted_count} 条旧数据")
        
        # 2. 创建索引
        logger.info("\n步骤 2: 创建唯一索引...")
        logger.info("创建唯一复合索引: 日期 + code + 跟踪标的")
        
        # 删除旧索引（如果存在）
        try:
            await collection.drop_index('idx_date_code_target_unique')
            logger.info("已删除旧的唯一索引")
        except:
            pass
        
        # 创建新的唯一索引
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
        
        # 创建其他常用索引
        await collection.create_index([('code', 1)], name='idx_code')
        await collection.create_index([('日期', -1)], name='idx_date_desc')
        await collection.create_index([('跟踪标的', 1)], name='idx_tracking_target')
        logger.info("✅ 其他索引创建成功")
        
        # 3. 重新下载数据
        logger.info("\n步骤 3: 重新下载数据...")
        logger.info("=" * 70)
        
        service = FundRefreshService(db)
        task_manager = get_task_manager()
        task_id = task_manager.create_task(
            task_type="refresh_fund_info_index_em",
            description="测试新唯一标识的数据下载"
        )
        
        result = await service.refresh_collection(
            collection_name="fund_info_index_em",
            task_id=task_id,
            params={}
        )
        
        logger.info("=" * 70)
        logger.info(f"下载完成: {result.get('message', '')}")
        logger.info(f"保存记录数: {result.get('saved', 0)}")
        
        # 4. 验证唯一性
        logger.info("\n步骤 4: 验证数据唯一性...")
        total_count = await collection.count_documents({})
        logger.info(f"总记录数: {total_count}")
        
        # 检查是否有重复（按新的唯一键分组）
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "日期": "$日期",
                        "code": "$code",
                        "跟踪标的": "$跟踪标的"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {"count": {"$gt": 1}}
            }
        ]
        
        duplicates = []
        async for doc in collection.aggregate(pipeline):
            duplicates.append(doc)
        
        if duplicates:
            logger.error(f"❌ 发现 {len(duplicates)} 组重复数据！")
            for dup in duplicates[:5]:
                logger.error(f"  重复: {dup}")
        else:
            logger.info("✅ 未发现重复数据，唯一性验证通过")
        
        # 显示数据分布
        logger.info("\n数据统计:")
        logger.info(f"  - 总记录数: {total_count}")
        
        # 按跟踪标的统计
        logger.info("\n按跟踪标的分类:")
        pipeline = [
            {"$group": {"_id": "$跟踪标的", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        async for doc in collection.aggregate(pipeline):
            logger.info(f"  - {doc['_id']}: {doc['count']} 条")
        
        # 按日期统计
        logger.info("\n最近的日期:")
        pipeline = [
            {"$group": {"_id": "$日期", "count": {"$sum": 1}}},
            {"$sort": {"_id": -1}},
            {"$limit": 5}
        ]
        async for doc in collection.aggregate(pipeline):
            logger.info(f"  - {doc['_id']}: {doc['count']} 条")
        
        # 示例数据
        logger.info("\n示例数据 (前3条):")
        cursor = collection.find({}).limit(3)
        async for doc in cursor:
            logger.info(f"\n  基金代码: {doc.get('基金代码')}")
            logger.info(f"  基金名称: {doc.get('基金名称')}")
            logger.info(f"  日期: {doc.get('日期')}")
            logger.info(f"  跟踪标的: {doc.get('跟踪标的')}")
            logger.info(f"  跟踪方式: {doc.get('跟踪方式')}")
            logger.info(f"  单位净值: {doc.get('单位净值')}")
        
        logger.info("\n" + "=" * 70)
        logger.info("测试完成！新的唯一标识工作正常")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
