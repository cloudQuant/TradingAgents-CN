"""
银行间市场债券发行数据服务（重构版）

数据集合名称: bond_debt_nafmii
"""
import asyncio

from app.services.data_sources.base_service import SimpleService
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager
from ..providers.bond_debt_nafmii_provider import BondDebtNafmiiProvider


class BondDebtNafmiiService(SimpleService):
    """银行间市场债券发行数据服务"""
    
    collection_name = "bond_debt_nafmii"
    provider_class = BondDebtNafmiiProvider

    async def update_batch_data(self, task_id: str = None, **kwargs):
        """批量更新：按页数循环调用 bond_debt_nafmii(page=...).

        前端通过 batch_update 传入 page_count（页数），这里将其解释为需要获取的页数，
        并逐页调用 provider.fetch_data(page=str(page))，避免将 page_count 直接传给 akshare。
        """
        task_manager = get_task_manager() if task_id else None

        page_count_value = kwargs.get("page_count")
        if page_count_value is None:
            page_count = 10
        else:
            try:
                page_count = int(page_count_value)
            except (TypeError, ValueError):
                raise ValueError(f"页数参数无效: {page_count_value}")

        # 限制页数范围，防止误操作（仅保证至少为 1 页，不再设置上限）
        if page_count < 1:
            page_count = 1

        if task_manager and task_id:
            task_manager.update_progress(
                task_id,
                0,
                100,
                f"开始获取前 {page_count} 页银行间市场债券发行数据...",
            )

        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)

        total_inserted = 0
        total_rows = 0
        success_pages = 0
        failed_pages = 0

        for page in range(1, page_count + 1):
            if task_manager and task_id:
                progress = 5 + int((page - 1) * 90 / max(page_count, 1))
                task_manager.update_progress(
                    task_id,
                    progress,
                    100,
                    f"正在获取第 {page}/{page_count} 页数据...",
                )

            try:
                # 在线程池中调用同步的 provider，显式只传入 page 参数
                df = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda p=page: self.provider.fetch_data(page=str(p)),
                )

                if df is None or df.empty:
                    continue

                df = self._reorder_dataframe_columns(df)
                total_rows += len(df)

                result = await control_db.save_dataframe_to_collection(
                    df,
                    extra_fields=extra_fields,
                )
                total_inserted += result.get("inserted", 0) + result.get("updated", 0)
                success_pages += 1

            except Exception as e:  # noqa: BLE001
                self.logger.error(
                    f"[{self.collection_name}] 获取第 {page} 页失败: {e}",
                    exc_info=True,
                )
                failed_pages += 1

        message_parts = [
            "批量更新完成",
            f"请求 {page_count} 页",
            f"成功 {success_pages} 页",
            f"保存 {total_inserted} 条记录",
        ]
        if failed_pages:
            message_parts.append(f"有 {failed_pages} 页更新失败")
        message = "，".join(message_parts)

        if task_manager and task_id:
            task_manager.update_progress(task_id, 100, 100, message)
            task_manager.complete_task(
                task_id,
                result={
                    "inserted": total_inserted,
                    "pages": page_count,
                    "success_pages": success_pages,
                    "failed_pages": failed_pages,
                    "rows": total_rows,
                },
                message=message,
            )

        return {
            "success": True,
            "message": message,
            "inserted": total_inserted,
            "pages": page_count,
            "success_pages": success_pages,
            "failed_pages": failed_pages,
            "rows": total_rows,
        }
