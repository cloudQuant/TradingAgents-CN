#!/usr/bin/env python3
"""
使用新的数据清理逻辑更新fund_info_index_em数据
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
        logger.info("初始化数据库...")
        await init_database()
        
        db = get_mongo_db()
        service = FundRefreshService(db)
        
        # 创建任务
        task_manager = get_task_manager()
        task_id = task_manager.create_task(
            task_type="refresh_fund_info_index_em",
            description="更新指数型基金基本信息"
        )
        
        logger.info(f"开始更新数据，任务ID: {task_id}")
        logger.info("=" * 60)
        
        # 执行更新
        result = await service.refresh_collection(
            collection_name="fund_info_index_em",
            task_id=task_id,
            params={}
        )
        
        logger.info("=" * 60)
        logger.info(f"更新完成:")
        logger.info(f"  - 成功: {result.get('success', False)}")
        logger.info(f"  - 保存记录数: {result.get('saved', 0)}")
        logger.info(f"  - 消息: {result.get('message', '')}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"更新失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
