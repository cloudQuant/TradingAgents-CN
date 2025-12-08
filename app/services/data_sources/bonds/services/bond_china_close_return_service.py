"""
收益率曲线历史数据服务（重构版）

数据集合名称: bond_china_close_return
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from app.services.data_sources.base_service import BaseService
from app.utils.task_manager import get_task_manager
from ..providers.bond_china_close_return_provider import BondChinaCloseReturnProvider


class BondChinaCloseReturnService(BaseService):
    """收益率曲线历史数据服务"""

    collection_name = "bond_china_close_return"
    provider_class = BondChinaCloseReturnProvider
    batch_concurrency = 3

    # 标准曲线名称列表（AkShare 需要中文名称作为 symbol 参数）
    # 这些是 bond_china_close_return 接口支持的曲线名称
    STANDARD_CURVE_NAMES = [
        "国债",
        "央行票据",
        "政策性金融债",
        "政策性金融债(国开行)",
        "政策性金融债(进出口行)",
        "政策性金融债(农发行)",
        "商业银行债",
        "商业银行普通债",
        "商业银行二级资本债",
        "商业银行无固定期限资本债",
        "企业债AAA",
        "企业债AA+",
        "企业债AA",
        "企业债AA-",
        "企业债A+",
        "中短期票据AAA",
        "中短期票据AA+",
        "中短期票据AA",
        "中短期票据AA-",
        "中短期票据A+",
        "同业存单AAA",
        "同业存单AA+",
        "同业存单AA",
        "地方政府债AAA",
        "资产支持证券AAA",
    ]

    async def _get_all_curve_names(self) -> List[str]:
        """获取所有曲线名称（使用标准中文名称列表）"""
        names: List[str] = []
        
        # 优先从数据库获取已有的曲线名称
        try:
            existing = await self.collection.distinct("曲线名称")
            for x in existing:
                if x and isinstance(x, str) and not x.startswith("CYCC"):  # 过滤掉代码格式
                    names.append(x)
            if names:
                self.logger.info(f"从数据库获取到 {len(names)} 条曲线名称")
        except Exception as e:
            self.logger.warning(f"从数据库获取曲线名称失败: {e}")

        # 尝试从 akshare 获取曲线名称映射
        try:
            import akshare as ak  # type: ignore

            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(None, ak.bond_china_close_return_map)
            if df is not None and not df.empty:
                self.logger.info(f"bond_china_close_return_map 返回列: {df.columns.tolist()}")
                self.logger.info(f"bond_china_close_return_map 前5行:\n{df.head()}")
                
                # 尝试找到中文名称列（通常是第二列或名为"曲线名称"/"名称"的列）
                name_col = None
                for candidate in ("曲线名称", "名称", "name", "curve_name"):
                    if candidate in df.columns:
                        name_col = candidate
                        break
                
                # 如果没找到，尝试使用第二列（通常第一列是代码，第二列是名称）
                if name_col is None and len(df.columns) >= 2:
                    name_col = df.columns[1]
                    self.logger.info(f"使用第二列作为曲线名称列: {name_col}")
                
                if name_col:
                    for val in df[name_col].dropna().tolist():
                        s = str(val).strip()
                        # 只接受中文名称，过滤掉代码格式（如 CYCC87C）
                        if s and not s.startswith("CYCC") and not s.isalnum():
                            names.append(s)
                    self.logger.info(f"从 akshare 提取到 {len(names)} 条中文曲线名称")
        except Exception as e:
            self.logger.warning(f"从 akshare 获取曲线名称失败: {e}")

        # 如果没有获取到有效的中文名称，使用标准列表
        if not names:
            self.logger.info("使用标准曲线名称列表")
            names = list(self.STANDARD_CURVE_NAMES)
        else:
            # 合并标准列表中的名称（确保常用曲线都被覆盖）
            for std_name in self.STANDARD_CURVE_NAMES:
                if std_name not in names:
                    names.append(std_name)

        return sorted(set(names))

    async def _get_latest_date_for_curve(self, curve_name: str) -> Optional[datetime]:
        doc = await self.collection.find_one({"曲线名称": curve_name}, sort=[("日期", -1)])
        if not doc:
            return None
        v = doc.get("日期")
        if v is None:
            return None
        if isinstance(v, datetime):
            return v
        text = str(v).split()[0]
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        return None

    def _split_date_range(self, start_dt: datetime, end_dt: datetime) -> List[Tuple[datetime, datetime]]:
        ranges: List[Tuple[datetime, datetime]] = []
        cur = start_dt
        while cur <= end_dt:
            seg_end = min(cur + timedelta(days=30), end_dt)
            ranges.append((cur, seg_end))
            cur = seg_end + timedelta(days=1)
        return ranges

    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        task_manager = get_task_manager() if task_id else None

        update_mode = str(kwargs.get("update_mode", "incremental") or "incremental")
        concurrency_val = kwargs.get("concurrency")
        try:
            concurrency = int(concurrency_val) if concurrency_val is not None else self.batch_concurrency
        except (TypeError, ValueError):
            concurrency = self.batch_concurrency
        if concurrency <= 0:
            concurrency = self.batch_concurrency

        if task_manager and task_id:
            task_manager.update_progress(task_id, 0, 100, "正在获取收益率曲线列表...")

        curve_names = await self._get_all_curve_names()
        if not curve_names:
            msg = "未获取到任何收益率曲线名称，无法执行批量更新"
            if task_manager and task_id:
                task_manager.fail_task(task_id, msg)
            return {"success": False, "message": msg, "inserted": 0}

        today = datetime.today().date()
        earliest = today - timedelta(days=90)

        tasks: List[Tuple[str, str, str]] = []
        for name in curve_names:
            latest_dt = None
            if update_mode != "full":
                latest_dt = await self._get_latest_date_for_curve(name)
            if latest_dt is None:
                start_date = earliest
            else:
                start_date = latest_dt.date() + timedelta(days=1)
                if start_date < earliest:
                    start_date = earliest
            if start_date > today:
                continue

            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(today, datetime.min.time())
            for s_dt, e_dt in self._split_date_range(start_dt, end_dt):
                s_str = s_dt.strftime("%Y%m%d")
                e_str = e_dt.strftime("%Y%m%d")
                tasks.append((name, s_str, e_str))

        if not tasks:
            msg = "所有曲线在近 3 个月内均已是最新，无需更新"
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, msg)
                task_manager.complete_task(task_id, result={"inserted": 0}, message=msg)
            return {"success": True, "message": msg, "inserted": 0}

        if task_manager and task_id:
            task_manager.update_progress(
                task_id,
                5,
                100,
                f"共 {len(curve_names)} 条曲线，拆分为 {len(tasks)} 个任务，开始批量更新...",
            )

        return await self._execute_batch_tasks(tasks, task_id, task_manager, concurrency)

    def get_batch_params(self, *args) -> Dict[str, Any]:
        if len(args) == 3:
            symbol, start_date, end_date = args
            return {
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
            }
        return super().get_batch_params(*args)
