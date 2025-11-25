"""
深交所期权数据服务
包含: option_current_day_szse, option_daily_stats_szse
"""

import akshare as ak
from typing import Dict, Any
from datetime import datetime, timedelta
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)


class OptionCurrentDaySzseService(BaseOptionService):
    """深交所当日合约服务"""
    
    collection_name = "option_current_day_szse"
    display_name = "深交所当日合约"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取深交所当日合约...")
            
            df = ak.option_current_day_szse()
            
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            records = df.to_dict('records')
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新深交所当日合约失败: {e}")
            return {"success": False, "message": str(e)}


class OptionDailyStatsSzseService(BaseOptionService):
    """深交所期权每日统计服务"""
    
    collection_name = "option_daily_stats_szse"
    display_name = "深交所期权每日统计"
    unique_fields = ["合约标识", "日期"]
    
    async def update_single_data(self, task_id: str = None, date: str = None, **kwargs) -> Dict[str, Any]:
        """更新指定日期的统计数据"""
        if not date:
            date = datetime.now().strftime("%Y%m%d")
        
        try:
            df = ak.option_daily_stats_szse(date=date)
            
            if df.empty:
                return {"success": True, "message": f"日期 {date} 无数据", "count": 0}
            
            df['日期'] = date
            records = df.to_dict('records')
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新深交所期权统计失败: {e}")
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, days: int = 5, **kwargs) -> Dict[str, Any]:
        """批量更新最近几个交易日的统计数据"""
        try:
            total_count = 0
            today = datetime.now()
            
            for i in range(days):
                date = (today - timedelta(days=i)).strftime("%Y%m%d")
                
                if self.task_manager and task_id:
                    progress = int((i / days) * 90) + 5
                    await self.task_manager.update_task(
                        task_id, 
                        progress=progress,
                        message=f"正在更新 {date} 的数据..."
                    )
                
                result = await self.update_single_data(date=date)
                if result.get("success"):
                    total_count += result.get("count", 0)
                
                await asyncio.sleep(0.2)
            
            return {
                "success": True,
                "message": f"批量更新完成，共更新 {days} 天，{total_count} 条数据",
                "count": total_count
            }
        except Exception as e:
            logger.error(f"批量更新深交所期权统计失败: {e}")
            return {"success": False, "message": str(e)}
