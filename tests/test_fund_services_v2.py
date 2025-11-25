"""
测试新的基金数据服务 V2
"""
import asyncio
import logging
from app.core.database import get_mongo_db
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2
from app.services.fund_data_service_v2 import FundDataServiceV2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_fund_name_em():
    """测试基金基本信息数据获取"""
    logger.info("=" * 50)
    logger.info("测试 fund_name_em 数据获取")
    logger.info("=" * 50)
    
    db = get_mongo_db()
    service = FundRefreshServiceV2(db)
    
    # 生成任务ID
    task_id = "test_fund_name_em_001"
    
    # 刷新数据
    try:
        result = await service.refresh_collection(
            collection_name="fund_name_em",
            task_id=task_id,
            params={}
        )
        logger.info(f"刷新结果: {result}")
        
        # 获取数据概览
        overview = await service.get_collection_overview("fund_name_em")
        logger.info(f"数据概览: {overview}")
        
        # 获取部分数据
        data = await service.get_collection_data("fund_name_em", limit=5)
        logger.info(f"数据样例: {data['data'][:2] if data['data'] else []}")
        
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)


async def test_fund_etf_spot():
    """测试ETF实时行情数据获取"""
    logger.info("=" * 50)
    logger.info("测试 fund_etf_spot_em 数据获取")
    logger.info("=" * 50)
    
    db = get_mongo_db()
    service = FundRefreshServiceV2(db)
    
    task_id = "test_fund_etf_spot_001"
    
    try:
        result = await service.refresh_collection(
            collection_name="fund_etf_spot_em",
            task_id=task_id,
            params={}
        )
        logger.info(f"刷新结果: {result}")
        
        overview = await service.get_collection_overview("fund_etf_spot_em")
        logger.info(f"数据概览: {overview}")
        
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)


async def test_data_service():
    """测试通用数据服务"""
    logger.info("=" * 50)
    logger.info("测试通用数据服务")
    logger.info("=" * 50)
    
    db = get_mongo_db()
    service = FundDataServiceV2(db)
    
    try:
        # 测试获取集合信息
        info = await service.get_collection_info("fund_name_em")
        logger.info(f"集合信息: {info}")
        
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)


async def main():
    """主测试函数"""
    # 测试基金基本信息
    await test_fund_name_em()
    
    # 测试ETF实时行情
    await test_fund_etf_spot()
    
    # 测试通用数据服务
    await test_data_service()


if __name__ == "__main__":
    asyncio.run(main())
