"""
地方债发行服务（重构版）

数据集合名称: bond_local_government_issue_cninfo
说明: 从巨潮资讯获取地方债发行数据，自动按最新发行起始日进行增量更新
"""
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from app.services.data_sources.base_service import BaseService
from app.services.database.control_mongodb import ControlMongodb
from ..providers.bond_local_government_issue_cninfo_provider import BondLocalGovernmentIssueCninfoProvider


class BondLocalGovernmentIssueCninfoService(BaseService):
    """地方债发行服务"""
    
    collection_name = "bond_local_government_issue_cninfo"
    provider_class = BondLocalGovernmentIssueCninfoProvider

    # 默认开始日期
    DEFAULT_START_DATE = "20000101"

    async def _get_latest_issue_date(self) -> Optional[str]:
        """从数据库获取最新的发行起始日"""
        try:
            doc = await self.collection.find_one({}, sort=[("发行起始日", -1)])
            if not doc:
                return None

            date_val = doc.get("发行起始日")
            if date_val is None:
                return None

            # 处理不同的日期格式
            if isinstance(date_val, datetime):
                next_day = date_val + timedelta(days=1)
                return next_day.strftime("%Y%m%d")

            date_str = str(date_val).split()[0]
            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
                try:
                    dt = datetime.strptime(date_str, fmt)
                    next_day = dt + timedelta(days=1)
                    return next_day.strftime("%Y%m%d")
                except ValueError:
                    continue

            return None
        except Exception as e:
            self.logger.warning(f"获取最新发行起始日失败: {e}")
            return None

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """更新地方债发行数据（自动增量）"""
        try:
            # 获取开始日期
            start_date = await self._get_latest_issue_date()

            if start_date is None:
                start_date = self.DEFAULT_START_DATE
                self.logger.info(f"数据库为空，使用默认开始日期: {start_date}")
            else:
                self.logger.info(f"从数据库获取到最新发行起始日，使用开始日期: {start_date}")

            # 当前日期作为结束日期
            end_date = datetime.today().strftime("%Y%m%d")

            if start_date > end_date:
                return {
                    "success": True,
                    "message": "数据已是最新，无需更新",
                    "inserted": 0,
                }

            self.logger.info(f"获取地方债发行数据: start_date={start_date}, end_date={end_date}")

            # 在线程池中调用 provider
            df = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.provider.fetch_data(start_date=start_date, end_date=end_date),
            )

            if df is None or df.empty:
                return {
                    "success": True,
                    "message": "没有新数据可更新",
                    "inserted": 0,
                }

            self.logger.info(f"获取到 {len(df)} 条地方债发行数据")

            # 按 field_info 顺序重排列
            df = self._reorder_dataframe_columns(df)

            # 保存到数据库
            unique_keys = self._get_unique_keys()
            extra_fields = self._get_extra_fields()

            control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)

            inserted = result.get("inserted", 0) + result.get("updated", 0)
            return {
                "success": result["success"],
                "message": f"成功更新 {inserted} 条地方债发行数据",
                "inserted": inserted,
                "details": result,
            }

        except Exception as e:
            self.logger.error(f"更新地方债发行数据失败: {e}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
