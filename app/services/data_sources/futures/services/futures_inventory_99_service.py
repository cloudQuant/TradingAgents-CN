"""库存数据-99期货网数据服务"""
import asyncio
from typing import Any, Dict, List

from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_inventory_99_provider import FuturesInventory99Provider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager


class FuturesInventory99Service(SimpleService):
    """库存数据-99期货网数据服务"""
    collection_name = "futures_inventory_99"
    provider_class = FuturesInventory99Provider

    DEFAULT_CONCURRENCY: int = 1

    @property
    def _symbol_list(self) -> List[str]:
        if hasattr(self.provider, "SYMBOL_LIST"):
            symbols = getattr(self.provider, "SYMBOL_LIST", None)
            if symbols:
                return list(symbols)
        return []

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        symbol = kwargs.get("symbol")
        symbols = self._symbol_list
        if symbol and symbols and symbol not in symbols:
            raise ValueError(f"不支持的品种: {symbol}")
        return await super().update_single_data(**kwargs)

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        task_manager = get_task_manager() if task_id else None

        concurrency_value = kwargs.get("concurrency")
        try:
            concurrency = int(concurrency_value) if concurrency_value is not None else self.DEFAULT_CONCURRENCY
        except (TypeError, ValueError):
            concurrency = self.DEFAULT_CONCURRENCY
        if concurrency < 1:
            concurrency = 1

        symbols = self._symbol_list

        if not symbols:
            message = "预设品种列表为空，无法执行批量更新"
            if task_manager and task_id:
                task_manager.fail_task(task_id, message)
            return {"success": False, "message": message, "inserted": 0}

        total_symbols = len(symbols)
        self.logger.info(
            f"[{self.collection_name}] 批量更新开始，共 {total_symbols} 个品种，将使用并发数 {concurrency}"
        )

        if task_manager and task_id:
            task_manager.update_progress(task_id, 5, 100, f"开始批量更新，共 {total_symbols} 个品种")

        semaphore = asyncio.Semaphore(concurrency)
        total_inserted = 0
        success_count = 0
        failed_count = 0
        lock = asyncio.Lock()

        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)

        async def process_symbol(symbol: str, index: int) -> None:
            nonlocal total_inserted, success_count, failed_count

            async with semaphore:
                try:
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda s=symbol: self.provider.fetch_data(symbol=s),
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

                if task_manager and task_id:
                    async with lock:
                        current_success = success_count
                        current_failed = failed_count
                        current_index = index + 1

                    progress = 10 + int(current_index / total_symbols * 85)
                    task_manager.update_progress(
                        task_id,
                        progress,
                        100,
                        f"已处理 {current_index}/{total_symbols}，成功 {current_success}，失败 {current_failed}",
                    )

        try:
            await asyncio.gather(*[process_symbol(s, i) for i, s in enumerate(symbols)])

            message = (
                f"批量更新完成：处理 {total_symbols} 个品种，"
                f"成功 {success_count}，失败 {failed_count}，保存 {total_inserted} 条"
            )

            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)

            return {"success": True, "message": message, "inserted": total_inserted}
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
