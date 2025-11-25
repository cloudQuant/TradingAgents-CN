"""
库存数据-东方财富服务
"""
import asyncio
import logging
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_inventory_em_provider import FuturesInventoryEmProvider
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)

# 东方财富库存数据支持的品种代码
DEFAULT_SYMBOLS = [
    "A", "B", "C", "CS", "M", "Y", "P", "I", "J", "JM", "JD",
    "L", "V", "PP", "EG", "EB", "PG", "LH", "RR",
    "CU", "AL", "ZN", "PB", "NI", "SN", "AU", "AG",
    "RB", "HC", "WR", "SS", "RU", "NR", "SP", "FU", "BU",
    "SR", "CF", "OI", "RM", "MA", "FG", "SA", "TA", "ZC",
    "AP", "CJ", "UR", "PK", "PF", "SI", "LC"
]


class FuturesInventoryEmService(BaseFuturesService):
    """库存数据-东方财富服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesInventoryEmProvider()
        super().__init__(db, "futures_inventory_em", provider)
    
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
            symbols: 品种代码列表，默认使用常用品种
            concurrency: 并发数，默认3
        """
        try:
            task_manager = get_task_manager() if task_id else None
            
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
                        
                        await asyncio.sleep(0.2)
                        
                    except Exception as e:
                        results["failed"] += 1
                        results["errors"].append({"symbol": symbol, "error": str(e)})
                        logger.error(f"更新品种 {symbol} 失败: {e}")
            
            tasks = [fetch_symbol(symbol, i) for i, symbol in enumerate(symbol_list)]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, total, total,
                    f"批量更新完成: 成功 {results['succeeded']}，失败 {results['failed']}，插入 {results['inserted']} 条"
                )
                task_manager.complete_task(task_id, result=results)
            
            logger.info(f"[{self.collection_name}] 批量更新完成: {results}")
            return results
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
