"""
库存数据-东方财富数据服务

支持批量更新：使用 ak.futures_inventory_em_varieties() 获取品种列表进行批量更新
"""
import asyncio
from typing import Any, Dict, List

from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_inventory_em_provider import FuturesInventoryEmProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager


class FuturesInventoryEmService(SimpleService):
    """库存数据-东方财富数据服务"""
    
    collection_name = "futures_inventory_em"
    provider_class = FuturesInventoryEmProvider
    
    time_field = "日期"
    unique_keys = ["品种代码", "日期"]
    
    DEFAULT_CONCURRENCY: int = 3
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新：使用 ak.futures_inventory_em_varieties() 获取品种列表
        """
        task_manager = get_task_manager() if task_id else None
        
        concurrency_value = kwargs.get("concurrency")
        try:
            concurrency = int(concurrency_value) if concurrency_value is not None else self.DEFAULT_CONCURRENCY
        except (TypeError, ValueError):
            concurrency = self.DEFAULT_CONCURRENCY
        if concurrency < 1:
            concurrency = 1
        
        try:
            # 获取品种列表
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, "正在获取品种列表...")
            
            symbols = await self._get_symbols_from_varieties()
            
            if not symbols:
                message = "未获取到品种列表"
                if task_manager and task_id:
                    task_manager.fail_task(task_id, message)
                return {"success": False, "message": message, "inserted": 0}
            
            total_symbols = len(symbols)
            self.logger.info(f"[{self.collection_name}] 获取到 {total_symbols} 个品种")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"需要更新 {total_symbols} 个品种")
            
            # 并发获取数据
            semaphore = asyncio.Semaphore(concurrency)
            total_inserted = 0
            success_count = 0
            failed_count = 0
            lock = asyncio.Lock()
            
            unique_keys = self._get_unique_keys()
            extra_fields = self._get_extra_fields()
            control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
            
            async def process_symbol(symbol: str, index: int):
                nonlocal total_inserted, success_count, failed_count
                
                async with semaphore:
                    try:
                        df = await asyncio.get_event_loop().run_in_executor(
                            None,
                            lambda s=symbol: self.provider.fetch_data(symbol=s)
                        )
                        
                        if df is not None and not df.empty:
                            df = self._reorder_dataframe_columns(df)
                            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
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
    
    async def _get_symbols_from_varieties(self) -> List[str]:
        """使用 ak.futures_inventory_em_varieties() 获取品种列表"""
        try:
            import akshare as ak
            
            df = await asyncio.get_event_loop().run_in_executor(
                None,
                ak.futures_inventory_em_varieties
            )
            
            if df is not None and not df.empty:
                # 获取品种代码列（通常是第一列或名为 '品种代码' 的列）
                if '品种代码' in df.columns:
                    symbols = df['品种代码'].dropna().unique().tolist()
                elif '品种' in df.columns:
                    symbols = df['品种'].dropna().unique().tolist()
                else:
                    # 取第一列作为品种代码
                    symbols = df.iloc[:, 0].dropna().unique().tolist()
                
                # 转换为字符串并过滤空值
                symbols = [str(s).strip() for s in symbols if s and str(s).strip()]
                return sorted(set(symbols))
            
            return []
            
        except Exception as e:
            self.logger.warning(f"[{self.collection_name}] 获取品种列表失败: {e}")
            return []
