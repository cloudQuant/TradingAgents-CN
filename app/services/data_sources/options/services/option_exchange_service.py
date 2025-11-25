"""
交易所商品期权数据服务
包含: option_hist_shfe, option_hist_dce, option_hist_czce, option_hist_gfex, option_czce_hist
"""

import akshare as ak
from typing import Dict, Any
from datetime import datetime, timedelta
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)

# 各交易所品种
SHFE_SYMBOLS = ["cu", "al", "zn", "au", "ag", "rb", "ru"]
DCE_SYMBOLS = ["m", "c", "i", "p", "y", "pp", "l"]
CZCE_SYMBOLS = ["SR", "CF", "TA", "MA", "RM", "OI"]
GFEX_SYMBOLS = ["si", "lc"]


class OptionHistShfeService(BaseOptionService):
    """上期所商品期权服务"""
    
    collection_name = "option_hist_shfe"
    display_name = "上期所商品期权"
    unique_fields = ["品种", "合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not trade_date:
            return {"success": False, "message": "缺少品种或交易日期参数"}
        try:
            df = ak.option_hist_shfe(symbol=symbol, trade_date=trade_date)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            df['日期'] = trade_date
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, days: int = 3, **kwargs) -> Dict[str, Any]:
        total_count = 0
        today = datetime.now()
        
        for symbol in SHFE_SYMBOLS[:3]:
            for i in range(days):
                trade_date = (today - timedelta(days=i)).strftime("%Y%m%d")
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, message=f"更新 {symbol} {trade_date}...")
                
                result = await self.update_single_data(symbol=symbol, trade_date=trade_date)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionHistDceService(BaseOptionService):
    """大商所商品期权服务"""
    
    collection_name = "option_hist_dce"
    display_name = "大商所商品期权"
    unique_fields = ["品种", "合约", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not trade_date:
            return {"success": False, "message": "缺少品种或交易日期参数"}
        try:
            df = ak.option_hist_dce(symbol=symbol, trade_date=trade_date)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            df['日期'] = trade_date
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, days: int = 3, **kwargs) -> Dict[str, Any]:
        total_count = 0
        today = datetime.now()
        
        for symbol in DCE_SYMBOLS[:3]:
            for i in range(days):
                trade_date = (today - timedelta(days=i)).strftime("%Y%m%d")
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, message=f"更新 {symbol} {trade_date}...")
                
                result = await self.update_single_data(symbol=symbol, trade_date=trade_date)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionHistCzceService(BaseOptionService):
    """郑商所商品期权服务"""
    
    collection_name = "option_hist_czce"
    display_name = "郑商所商品期权"
    unique_fields = ["品种", "合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not trade_date:
            return {"success": False, "message": "缺少品种或交易日期参数"}
        try:
            df = ak.option_hist_czce(symbol=symbol, trade_date=trade_date)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            df['日期'] = trade_date
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, days: int = 3, **kwargs) -> Dict[str, Any]:
        total_count = 0
        today = datetime.now()
        
        for symbol in CZCE_SYMBOLS[:3]:
            for i in range(days):
                trade_date = (today - timedelta(days=i)).strftime("%Y%m%d")
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, message=f"更新 {symbol} {trade_date}...")
                
                result = await self.update_single_data(symbol=symbol, trade_date=trade_date)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionHistGfexService(BaseOptionService):
    """广期所商品期权服务"""
    
    collection_name = "option_hist_gfex"
    display_name = "广期所商品期权"
    unique_fields = ["品种", "合约名称", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not trade_date:
            return {"success": False, "message": "缺少品种或交易日期参数"}
        try:
            df = ak.option_hist_gfex(symbol=symbol, trade_date=trade_date)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            df['日期'] = trade_date
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, days: int = 3, **kwargs) -> Dict[str, Any]:
        total_count = 0
        today = datetime.now()
        
        for symbol in GFEX_SYMBOLS:
            for i in range(days):
                trade_date = (today - timedelta(days=i)).strftime("%Y%m%d")
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, message=f"更新 {symbol} {trade_date}...")
                
                result = await self.update_single_data(symbol=symbol, trade_date=trade_date)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


# 郑商所历史期权品种代码映射
CZCE_HIST_SYMBOLS = {
    "白糖": "SR", "棉花": "CF", "PTA": "TA", "甲醇": "MA", 
    "菜籽粕": "RM", "动力煤": "ZC", "菜籽油": "OI", "花生": "PK",
    "对二甲苯": "PX", "烧碱": "SH", "纯碱": "SA", "短纤": "PF",
    "锰硅": "SM", "硅铁": "SF", "尿素": "UR", "苹果": "AP",
    "红枣": "CJ", "玻璃": "FG", "瓶片": "PR"
}


class OptionCzceHistService(BaseOptionService):
    """郑商所期权历史行情服务（按年度获取）"""
    
    collection_name = "option_czce_hist"
    display_name = "郑商所期权历史行情"
    unique_fields = ["品种代码", "交易日期"]
    
    async def update_single_data(self, task_id: str = None, year: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not year:
            year = str(datetime.now().year)
        if not symbol:
            return {"success": False, "message": "缺少品种代码参数（如 SR, CF, TA）"}
        try:
            df = ak.option_czce_hist(year=year, symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['年份'] = year
            df['品种代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新当年主要品种的历史行情"""
        total_count = 0
        year = str(datetime.now().year)
        symbols = list(CZCE_HIST_SYMBOLS.values())[:5]  # 取前5个品种
        
        for i, symbol in enumerate(symbols):
            if self.task_manager and task_id:
                progress = int((i / len(symbols)) * 90) + 5
                await self.task_manager.update_task(task_id, progress=progress, message=f"更新 {symbol} {year}年数据...")
            
            result = await self.update_single_data(year=year, symbol=symbol)
            if result.get("success"):
                total_count += result.get("count", 0)
            await asyncio.sleep(0.5)
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
