"""
Symbol批量更新服务基类

为需要symbol参数的期货数据集合提供从其他集合获取symbol列表进行批量更新的功能
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import asyncio

from app.services.data_sources.base_service import BaseService
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class SymbolBatchService(BaseService):
    """
    Symbol批量更新服务基类
    
    子类需要定义：
    - collection_name: 集合名称
    - provider_class: Provider类
    - SYMBOL_SOURCE_COLLECTION: symbol来源集合名称
    - SYMBOL_SOURCE_FIELD: symbol来源字段名称
    """
    
    # symbol来源配置（子类必须覆盖）
    SYMBOL_SOURCE_COLLECTION = "futures_fees_info"
    SYMBOL_SOURCE_FIELD = "品种代码"
    
    # 默认配置
    time_field = "更新时间"
    
    # API调用间隔（秒）
    API_DELAY = 0.2
    
    # 并发数
    CONCURRENCY = 3
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新
        
        从配置的源集合获取symbol列表，逐个获取数据
        """
        task_manager = get_task_manager() if task_id else None
        
        try:
            # 获取symbol列表
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, f"正在从 {self.SYMBOL_SOURCE_COLLECTION} 获取品种列表...")
            
            symbols = await self._get_symbols()
            
            if not symbols:
                message = f"未找到品种列表，请先更新 {self.SYMBOL_SOURCE_COLLECTION} 集合"
                if task_manager and task_id:
                    task_manager.fail_task(task_id, message)
                return {"success": False, "message": message, "inserted": 0}
            
            total_symbols = len(symbols)
            self.logger.info(f"[{self.collection_name}] 获取到 {total_symbols} 个品种")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"需要更新 {total_symbols} 个品种")
            
            # 并发获取数据
            semaphore = asyncio.Semaphore(self.CONCURRENCY)
            total_inserted = 0
            success_count = 0
            failed_count = 0
            lock = asyncio.Lock()
            
            async def process_symbol(symbol: str, index: int):
                nonlocal total_inserted, success_count, failed_count
                
                async with semaphore:
                    try:
                        # 获取数据
                        df = await asyncio.get_event_loop().run_in_executor(
                            None,
                            lambda s=symbol: self.provider.fetch_data(symbol=s)
                        )
                        
                        if df is not None and not df.empty:
                            # 保存数据
                            unique_keys = self._get_unique_keys()
                            control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
                            result = await control_db.save_dataframe_to_collection(df)
                            inserted = result.get("inserted", 0) + result.get("updated", 0)
                            
                            async with lock:
                                total_inserted += inserted
                                success_count += 1
                            
                            self.logger.debug(f"[{self.collection_name}] {symbol}: 保存 {inserted} 条")
                        else:
                            self.logger.debug(f"[{self.collection_name}] {symbol}: 无数据")
                        
                    except Exception as e:
                        async with lock:
                            failed_count += 1
                        self.logger.warning(f"[{self.collection_name}] {symbol} 获取失败: {e}")
                    
                    # 更新进度
                    if task_manager and task_id:
                        async with lock:
                            current_success = success_count
                            current_failed = failed_count
                        
                        progress = 10 + int((index + 1) / total_symbols * 85)
                        task_manager.update_progress(
                            task_id, progress, 100,
                            f"已处理 {index + 1}/{total_symbols}，成功 {current_success}，失败 {current_failed}"
                        )
                    
                    # 控制API调用频率
                    await asyncio.sleep(self.API_DELAY)
            
            # 并发执行
            await asyncio.gather(*[process_symbol(s, i) for i, s in enumerate(symbols)])
            
            message = f"批量更新完成：处理 {total_symbols} 个品种，成功 {success_count}，失败 {failed_count}，保存 {total_inserted} 条"
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)
            
            return {"success": True, "message": message, "inserted": total_inserted}
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
    
    async def _get_symbols(self) -> List[str]:
        """从源集合获取symbol列表"""
        try:
            source_collection = self.db[self.SYMBOL_SOURCE_COLLECTION]
            
            # 获取不重复的symbol
            symbols = await source_collection.distinct(self.SYMBOL_SOURCE_FIELD)
            
            # 过滤空值
            symbols = [s for s in symbols if s and str(s).strip()]
            
            return sorted(set(symbols))
            
        except Exception as e:
            self.logger.warning(f"[{self.collection_name}] 获取symbol列表失败: {e}")
            return []
