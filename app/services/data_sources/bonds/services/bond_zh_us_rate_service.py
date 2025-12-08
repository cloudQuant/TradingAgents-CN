"""
中美国债收益率服务（重构版）

数据集合名称: bond_zh_us_rate
说明: 从东方财富网获取中美国债收益率历史数据，数据从 19901219 开始
      更新时自动获取数据库中最新日期，从该日期开始增量获取数据
"""
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from app.services.data_sources.base_service import BaseService
from app.services.database.control_mongodb import ControlMongodb
from ..providers.bond_zh_us_rate_provider import BondZhUsRateProvider


class BondZhUsRateService(BaseService):
    """中美国债收益率服务"""
    
    collection_name = "bond_zh_us_rate"
    provider_class = BondZhUsRateProvider

    # 默认开始日期（数据最早可追溯日期）
    DEFAULT_START_DATE = "19901219"

    async def _get_latest_date(self) -> Optional[str]:
        """从数据库获取最新日期"""
        try:
            doc = await self.collection.find_one({}, sort=[("日期", -1)])
            if not doc:
                return None
            
            date_val = doc.get("日期")
            if date_val is None:
                return None
            
            # 处理不同的日期格式
            if isinstance(date_val, datetime):
                # 返回下一天作为开始日期
                next_day = date_val + timedelta(days=1)
                return next_day.strftime("%Y%m%d")
            
            # 字符串格式
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
            self.logger.warning(f"获取最新日期失败: {e}")
            return None

    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新中美国债收益率数据
        
        自动从数据库获取最新日期，然后从该日期开始增量获取数据
        如果数据库为空，则从 19901219 开始获取
        """
        try:
            # 获取数据库中最新日期
            start_date = await self._get_latest_date()
            
            if start_date is None:
                start_date = self.DEFAULT_START_DATE
                self.logger.info(f"数据库为空，使用默认开始日期: {start_date}")
            else:
                self.logger.info(f"从数据库获取到最新日期，使用开始日期: {start_date}")
            
            # 检查开始日期是否已超过今天
            today = datetime.today().strftime("%Y%m%d")
            if start_date > today:
                return {
                    "success": True,
                    "message": "数据已是最新，无需更新",
                    "inserted": 0,
                }
            
            # 在线程池中调用 provider 获取数据
            df = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.provider.fetch_data(start_date=start_date)
            )
            
            if df is None or df.empty:
                return {
                    "success": True,
                    "message": "没有新数据可更新",
                    "inserted": 0,
                }
            
            self.logger.info(f"获取到 {len(df)} 条数据")
            
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
                "message": f"成功更新 {inserted} 条数据",
                "inserted": inserted,
                "details": result,
            }
            
        except Exception as e:
            self.logger.error(f"更新中美国债收益率数据失败: {e}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
