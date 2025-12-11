"""货币报价历史数据服务"""
import asyncio
from datetime import datetime, timedelta

from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.currencies.providers.currency_history_provider import (
    CurrencyHistoryProvider,
)
from app.utils.task_manager import get_task_manager


class CurrencyHistoryService(SimpleService):
    """货币报价历史数据服务"""

    collection_name = "currency_history"
    provider_class = CurrencyHistoryProvider

    async def update_batch_data(self, task_id: str = None, **kwargs):  # type: ignore[override]
        """按日批量更新历史汇率

        批量更新参数：
        - base: 基础货币（可选，默认 USD）
        - start_date: 开始日期，格式 YYYY-MM-DD，必填
        - api_key: CurrencyScoop API Key，必填
        - concurrency: 并发数，可选，默认 3

        逻辑：
        1. 解析开始日期，从 start_date 一直到当前日期（含）生成日期列表
        2. 按并发数限制，同时对每个日期调用一次单日更新（update_single_data）
        3. 聚合插入/更新条数，并通过 TaskManager 汇报进度
        """

        task_manager = get_task_manager() if task_id else None

        # 过滤掉只用于前端控制的参数
        frontend_only_params = {
            "update_type",
            "update_mode",
            "batch_update",
            "batch_size",
            "page",
            "limit",
            "skip",
            "filters",
            "sort",
            "order",
            "task_id",
            "callback",
            "async",
            "timeout",
            "_t",
            "_timestamp",
            "force",
            "clear_first",
            "overwrite",
            "mode",
        }

        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in frontend_only_params}

        # 并发数（前端可配置，默认使用 BaseService.batch_concurrency=3）
        concurrency_value = filtered_kwargs.pop("concurrency", None)
        try:
            concurrency = (
                int(concurrency_value)
                if concurrency_value is not None
                else self.batch_concurrency
            )
        except (TypeError, ValueError):
            concurrency = self.batch_concurrency

        # 开始日期参数
        start_date_str = filtered_kwargs.pop("start_date", None)
        if not start_date_str:
            raise ValueError("缺少必须参数: start_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                f"开始日期格式错误: {start_date_str}，期望格式为 YYYY-MM-DD"
            )

        today = datetime.utcnow().date()
        if start_date > today:
            raise ValueError("开始日期不能晚于当前日期")

        total_days = (today - start_date).days + 1
        date_list = [start_date + timedelta(days=i) for i in range(total_days)]
        date_strs = [d.strftime("%Y-%m-%d") for d in date_list]

        if not date_strs:
            return {
                "success": True,
                "message": "没有需要更新的日期",
                "inserted": 0,
                "processed_days": 0,
                "success_days": 0,
                "failed_days": 0,
            }

        self.logger.info(
            f"[currency_history] 批量更新，从 {start_date_str} 到 {today.strftime('%Y-%m-%d')}，共 {total_days} 天，"
            f"并发数={concurrency}，参数={filtered_kwargs}"
        )

        if task_manager and task_id:
            task_manager.update_progress(
                task_id,
                5,
                100,
                f"准备从 {start_date_str} 到 {today.strftime('%Y-%m-%d')} 共 {total_days} 天历史汇率...",
            )

        semaphore = asyncio.Semaphore(max(1, concurrency))
        lock = asyncio.Lock()

        processed = 0
        success_days = 0
        failed_days = 0
        total_inserted = 0

        async def process_date(date_str: str):
            nonlocal processed, success_days, failed_days, total_inserted
            async with semaphore:
                try:
                    # 对每个日期调用单日更新
                    params = dict(filtered_kwargs)
                    params["date"] = date_str

                    result = await self.update_single_data(**params)

                    async with lock:
                        processed += 1
                        if result.get("success"):
                            success_days += 1
                            total_inserted += int(result.get("inserted", 0) or 0)
                        else:
                            failed_days += 1

                        if task_manager and task_id:
                            progress = (
                                10 + int(processed / total_days * 85)
                                if total_days > 0
                                else 95
                            )
                            msg = (
                                f"已处理 {processed}/{total_days} 天，"
                                f"成功 {success_days} 天，失败 {failed_days} 天"
                            )
                            task_manager.update_progress(task_id, progress, 100, msg)

                except Exception as e:  # noqa: BLE001
                    self.logger.error(
                        f"[currency_history] 处理日期 {date_str} 失败: {e}",
                        exc_info=True,
                    )
                    async with lock:
                        processed += 1
                        failed_days += 1
                        if task_manager and task_id:
                            progress = (
                                10 + int(processed / total_days * 85)
                                if total_days > 0
                                else 95
                            )
                            msg = (
                                f"已处理 {processed}/{total_days} 天，"
                                f"成功 {success_days} 天，失败 {failed_days} 天"
                            )
                            task_manager.update_progress(task_id, progress, 100, msg)

        try:
            await asyncio.gather(*(process_date(d) for d in date_strs))
        except Exception as e:  # noqa: BLE001
            # 顶层异常捕获，防止任务挂死
            self.logger.error(f"[currency_history] 批量更新执行失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": total_inserted,
                "processed_days": processed,
                "success_days": success_days,
                "failed_days": failed_days,
            }

        message = (
            f"批量更新完成，从 {start_date_str} 到 {today.strftime('%Y-%m-%d')}，共处理 {processed} 天，"
            f"成功 {success_days} 天，失败 {failed_days} 天，插入/更新 {total_inserted} 条记录"
        )

        self.logger.info(f"[currency_history] {message}")

        if task_manager and task_id:
            task_manager.update_progress(task_id, 100, 100, message)
            task_manager.complete_task(
                task_id,
                result={
                    "inserted": total_inserted,
                    "processed_days": processed,
                    "success_days": success_days,
                    "failed_days": failed_days,
                    "start_date": start_date_str,
                    "end_date": today.strftime("%Y-%m-%d"),
                    "concurrency": concurrency,
                },
                message=message,
            )

        return {
            "success": True,
            "message": message,
            "inserted": total_inserted,
            "processed_days": processed,
            "success_days": success_days,
            "failed_days": failed_days,
        }
