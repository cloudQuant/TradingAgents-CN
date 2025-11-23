#!/usr/bin/env python3
"""
测试优化后的基金数据下载方式
遍历所有参数组合获取数据
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """主函数"""
    try:
        logger.info("=" * 70)
        logger.info("测试优化后的基金数据下载方式")
        logger.info("=" * 70)
        
        logger.info("初始化数据库...")
        await init_database()
        
        db = get_mongo_db()
        service = FundRefreshService(db)
        
        # 创建任务
        task_manager = get_task_manager()
        task_id = task_manager.create_task(
            task_type="refresh_fund_info_index_em",
            description="测试优化的指数型基金数据下载"
        )
        
        logger.info(f"任务ID: {task_id}")
        logger.info("=" * 70)
        logger.info("开始下载数据...")
        logger.info("将遍历以下参数组合：")
        logger.info("  Symbol: 沪深指数, 行业主题, 大盘指数, 中盘指数, 小盘指数, 股票指数, 债券指数")
        logger.info("  Indicator: 被动指数型, 增强指数型")
        logger.info("  总计: 7 x 2 = 14 个组合")
        logger.info("=" * 70)
        
        # 执行更新
        result = await service.refresh_collection(
            collection_name="fund_info_index_em",
            task_id=task_id,
            params={}
        )
        
        logger.info("=" * 70)
        logger.info("下载完成！")
        logger.info(f"  - 成功: {result.get('success', False)}")
        logger.info(f"  - 保存记录数: {result.get('saved', 0)}")
        logger.info(f"  - 遍历组合数: {result.get('total_combinations', 0)}")
        logger.info(f"  - 消息: {result.get('message', '')}")
        logger.info("=" * 70)
        
        # 查询数据库统计
        collection = db.get_collection('fund_info_index_em')
        total_count = await collection.count_documents({})
        logger.info(f"数据库中总记录数: {total_count}")
        
        # 统计各分类的数量
        logger.info("\n按跟踪标的分类统计:")
        pipeline = [
            {"$group": {"_id": "$跟踪标的", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        async for doc in collection.aggregate(pipeline):
            标的 = doc.get('_id', '未知')
            数量 = doc.get('count', 0)
            logger.info(f"  - {标的}: {数量} 条")
        
        logger.info("\n按跟踪方式分类统计:")
        pipeline = [
            {"$group": {"_id": "$跟踪方式", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        async for doc in collection.aggregate(pipeline):
            方式 = doc.get('_id', '未知')
            数量 = doc.get('count', 0)
            logger.info(f"  - {方式}: {数量} 条")
        
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
