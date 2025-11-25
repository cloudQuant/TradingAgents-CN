"""
金融期权数据服务
包含: option_finance_board
"""

import akshare as ak
from typing import Dict, Any
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)

FINANCE_SYMBOLS = [
    "华夏上证50ETF期权", "华泰柏瑞沪深300ETF期权", "嘉实沪深300ETF期权",
    "沪深300股指期权", "中证1000股指期权", "上证50股指期权"
]


class OptionFinanceBoardService(BaseOptionService):
    """金融期权行情数据服务"""
    
    collection_name = "option_finance_board"
    display_name = "金融期权行情数据"
    unique_fields = ["品种", "到期月份", "合约代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, end_month: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not end_month:
            return {"success": False, "message": "缺少品种或到期月份参数"}
        try:
            df = ak.option_finance_board(symbol=symbol, end_month=end_month)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            df['到期月份'] = end_month
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            logger.error(f"更新金融期权行情失败: {e}")
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新所有品种近4个月的行情"""
        try:
            from datetime import datetime
            
            # 生成近4个月的到期月份
            now = datetime.now()
            months = []
            for i in range(4):
                month = now.month + i
                year = now.year
                if month > 12:
                    month -= 12
                    year += 1
                months.append(f"{str(year)[2:]}{month:02d}")
            
            total_count = 0
            total_tasks = len(FINANCE_SYMBOLS) * len(months)
            completed = 0
            
            for symbol in FINANCE_SYMBOLS:
                for end_month in months:
                    if self.task_manager and task_id:
                        progress = int((completed / total_tasks) * 90) + 5
                        await self.task_manager.update_task(
                            task_id, progress=progress,
                            message=f"更新 {symbol} {end_month}..."
                        )
                    
                    try:
                        result = await self.update_single_data(symbol=symbol, end_month=end_month)
                        if result.get("success"):
                            total_count += result.get("count", 0)
                    except Exception as e:
                        logger.warning(f"更新 {symbol} {end_month} 失败: {e}")
                    
                    completed += 1
                    await asyncio.sleep(0.2)
            
            return {
                "success": True,
                "message": f"批量更新完成，共 {total_count} 条",
                "count": total_count
            }
        except Exception as e:
            logger.error(f"批量更新金融期权行情失败: {e}")
            return {"success": False, "message": str(e)}


class OptionFinanceMinuteSinaService(BaseOptionService):
    """新浪金融期权分时行情服务"""
    
    collection_name = "option_finance_minute_sina"
    display_name = "新浪期权分时行情"
    unique_fields = ["合约代码", "时间"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_finance_minute_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "请使用单条更新，需要指定合约代码"}
