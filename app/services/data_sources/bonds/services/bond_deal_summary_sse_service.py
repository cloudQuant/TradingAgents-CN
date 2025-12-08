"""
债券成交概览-上交所服务（重构版）

数据集合名称: bond_deal_summary_sse
"""
from datetime import datetime, timedelta
import asyncio

from app.services.data_sources.base_service import BaseService
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager
from ..providers.bond_deal_summary_sse_provider import BondDealSummarySseProvider


class BondDealSummarySseService(BaseService):
    """债券成交概览-上交所服务"""
    
    collection_name = "bond_deal_summary_sse"
    provider_class = BondDealSummarySseProvider

    async def update_batch_data(self, task_id: str = None, **kwargs):
        """批量更新：按日期范围逐日调用 bond_deal_summary_sse(date=...).

        前端通过 batch_update 传入 start_date / end_date（格式 YYYYMMDD 或 YYYY-MM-DD），
        这里将其展开为一系列单日调用，避免将 start_date 直接传给 akshare。
        """
        task_manager = get_task_manager() if task_id else None

        # 提取并规范化日期参数
        start_date = kwargs.get("start_date") or kwargs.get("date")
        end_date = kwargs.get("end_date") or kwargs.get("date")

        def _parse_date(value):
            if not value:
                return None
            s = str(value).strip()
            if not s:
                return None
            if "-" in s:
                s = s.replace("-", "")
            if len(s) != 8 or not s.isdigit():
                raise ValueError(f"日期格式无效: {value}，需要 YYYYMMDD 或 YYYY-MM-DD")
            return datetime.strptime(s, "%Y%m%d")

        if not start_date and not end_date:
            # 未提供任何日期时，默认只更新当日
            start_dt = end_dt = datetime.now()
        else:
            start_dt = _parse_date(start_date) if start_date else _parse_date(end_date)
            end_dt = _parse_date(end_date) if end_date else start_dt

        if start_dt > end_dt:
            start_dt, end_dt = end_dt, start_dt

        total_days = (end_dt - start_dt).days + 1

        if task_manager and task_id:
            task_manager.update_progress(
                task_id,
                0,
                100,
                f"开始更新 {total_days} 个交易日的债券成交概览...",
            )

        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)

        total_inserted = 0
        total_rows = 0
        failed_days = 0

        current_dt = start_dt
        for idx in range(total_days):
            date_str = current_dt.strftime("%Y%m%d")

            if task_manager and task_id:
                progress = 5 + int(idx * 90 / max(total_days, 1))
                task_manager.update_progress(
                    task_id,
                    progress,
                    100,
                    f"正在更新 {date_str} 的数据 ({idx + 1}/{total_days})...",
                )

            try:
                # 在线程池中调用同步的 provider，显式只传入 date 参数
                df = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda d=date_str: self.provider.fetch_data(date=d),
                )

                if df is None or df.empty:
                    current_dt += timedelta(days=1)
                    continue

                # 按 field_info 重新排列列顺序
                df = self._reorder_dataframe_columns(df)
                total_rows += len(df)

                result = await control_db.save_dataframe_to_collection(
                    df,
                    extra_fields=extra_fields,
                )
                total_inserted += result.get("inserted", 0) + result.get("updated", 0)

            except Exception as e:  # noqa: BLE001
                self.logger.error(
                    f"[{self.collection_name}] 更新 {date_str} 失败: {e}",
                    exc_info=True,
                )
                failed_days += 1

            current_dt += timedelta(days=1)

        message_parts = [
            "批量更新完成",
            f"覆盖 {total_days} 天",
            f"保存 {total_inserted} 条记录",
        ]
        if failed_days:
            message_parts.append(f"有 {failed_days} 天更新失败")
        message = "，".join(message_parts)

        if task_manager and task_id:
            task_manager.update_progress(task_id, 100, 100, message)
            task_manager.complete_task(
                task_id,
                result={
                    "inserted": total_inserted,
                    "days": total_days,
                    "failed_days": failed_days,
                    "rows": total_rows,
                },
                message=message,
            )

        return {
            "success": True,
            "message": message,
            "inserted": total_inserted,
            "days": total_days,
            "failed_days": failed_days,
            "rows": total_rows,
        }
