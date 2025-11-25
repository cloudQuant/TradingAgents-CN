"""
库存数据-99期货网服务
"""
import asyncio
import logging
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_inventory_99_provider import FuturesInventory99Provider
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)

# 常用期货品种列表
DEFAULT_SYMBOLS = [
    "豆一", "豆二", "豆粕", "豆油", "玉米", "玉米淀粉", "棕榈油",
    "铁矿石", "焦炭", "焦煤", "鸡蛋", "聚乙烯", "聚氯乙烯", "聚丙烯",
    "乙二醇", "苯乙烯", "液化石油气", "生猪",
    "铜", "铝", "锌", "铅", "镍", "锡", "黄金", "白银",
    "螺纹钢", "热轧卷板", "线材", "不锈钢", "天然橡胶", "纸浆", "燃料油", "沥青",
    "白糖", "棉花", "菜籽油", "菜粕", "甲醇", "玻璃", "纯碱", "PTA",
    "动力煤", "苹果", "红枣", "尿素", "花生",
    "工业硅", "碳酸锂"
]


class FuturesInventory99Service(BaseFuturesService):
    """库存数据-99期货网服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesInventory99Provider()
        super().__init__(db, "futures_inventory_99", provider)
    
    async def update_batch_data(
        self, 
        task_id: str = None,
        symbols: List[str] = None,
        concurrency: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        批量更新多个品种的库存数据
        
        Args:
            task_id: 任务ID
            symbols: 品种列表，默认使用常用品种
            concurrency: 并发数，默认3
        """
        try:
            task_manager = get_task_manager() if task_id else None
            
            # 使用传入的品种列表或默认列表
            symbol_list = symbols if symbols else DEFAULT_SYMBOLS
            total = len(symbol_list)
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, total, f"准备更新 {total} 个品种的库存数据...")
            
            logger.info(f"[{self.collection_name}] 开始批量更新 {total} 个品种")
            
            results = {
                "success": True,
                "total": total,
                "succeeded": 0,
                "failed": 0,
                "inserted": 0,
                "errors": []
            }
            
            # 使用信号量控制并发
            semaphore = asyncio.Semaphore(concurrency)
            
            async def fetch_symbol(symbol: str, index: int):
                async with semaphore:
                    try:
                        result = await self.update_single_data(symbol=symbol)
                        if result.get("success"):
                            results["succeeded"] += 1
                            results["inserted"] += result.get("inserted", 0)
                        else:
                            results["failed"] += 1
                            results["errors"].append({"symbol": symbol, "error": result.get("message")})
                        
                        if task_manager and task_id:
                            task_manager.update_progress(
                                task_id, index + 1, total,
                                f"已完成 {symbol}，进度 {index + 1}/{total}"
                            )
                        
                        # 添加延迟避免API限流
                        await asyncio.sleep(0.2)
                        
                    except Exception as e:
                        results["failed"] += 1
                        results["errors"].append({"symbol": symbol, "error": str(e)})
                        logger.error(f"更新品种 {symbol} 失败: {e}")
            
            # 并发执行
            tasks = [fetch_symbol(symbol, i) for i, symbol in enumerate(symbol_list)]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 更新任务状态
            if task_manager and task_id:
                if results["failed"] == 0:
                    task_manager.update_progress(
                        task_id, total, total,
                        f"批量更新完成: 成功 {results['succeeded']} 个品种，插入 {results['inserted']} 条数据"
                    )
                    task_manager.complete_task(task_id, result=results)
                else:
                    task_manager.update_progress(
                        task_id, total, total,
                        f"批量更新完成: 成功 {results['succeeded']}，失败 {results['failed']}"
                    )
                    task_manager.complete_task(task_id, result=results)
            
            logger.info(f"[{self.collection_name}] 批量更新完成: {results}")
            return results
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
