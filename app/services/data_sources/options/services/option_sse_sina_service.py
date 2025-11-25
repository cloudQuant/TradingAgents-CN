"""
上交所ETF期权服务 (新浪)
包含: option_sse_list_sina, option_sse_expire_day_sina, option_sse_codes_sina,
      option_sse_underlying_spot_price_sina, option_sse_greeks_sina,
      option_sse_minute_sina, option_sse_daily_sina
"""

import akshare as ak
from typing import Dict, Any
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)

ETF_SYMBOLS = ["50ETF", "300ETF"]


class OptionSseListSinaService(BaseOptionService):
    """上交所ETF合约到期月份服务"""
    
    collection_name = "option_sse_list_sina"
    display_name = "上交所ETF合约到期月份"
    unique_fields = ["品种", "到期月份"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, exchange: str = "null", **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少品种参数（如 50ETF 或 300ETF）"}
        try:
            # akshare参数: symbol, exchange
            result_list = ak.option_sse_list_sina(symbol=symbol, exchange=exchange)
            if not result_list:
                return {"success": True, "message": "无数据", "count": 0}
            
            # 返回结果为列表
            records = [{"品种": symbol, "到期月份": month} for month in result_list]
            await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        total_count = 0
        for symbol in ETF_SYMBOLS:
            result = await self.update_single_data(symbol=symbol, exchange="null")
            if result.get("success"):
                total_count += result.get("count", 0)
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionSseExpireDaySinaService(BaseOptionService):
    """上交所ETF剩余到期时间服务"""
    
    collection_name = "option_sse_expire_day_sina"
    display_name = "上交所ETF剩余到期时间"
    unique_fields = ["品种", "到期月份"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not trade_date:
            return {"success": False, "message": "缺少品种(50ETF/300ETF)或到期月份(trade_date如202002)参数"}
        try:
            # akshare参数: trade_date, symbol, exchange
            result_data = ak.option_sse_expire_day_sina(trade_date=trade_date, symbol=symbol, exchange="null")
            # 返回结果为元组 (到期日, 剩余天数)
            expire_date, days_left = result_data if isinstance(result_data, tuple) else (None, result_data)
            record = {"品种": symbol, "到期月份": trade_date, "到期日": expire_date, "剩余天数": days_left}
            await self._save_data([record])
            return {"success": True, "message": "更新完成", "count": 1}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        total_count = 0
        for symbol in ETF_SYMBOLS:
            try:
                months = ak.option_sse_list_sina(symbol=symbol, exchange="null")
                for month in months[:4]:  # 最近4个月
                    result = await self.update_single_data(symbol=symbol, trade_date=month)
                    if result.get("success"):
                        total_count += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"获取 {symbol} 到期时间失败: {e}")
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


UNDERLYING_CODES = ["510050", "510300"]  # 50ETF和300ETF的代码


class OptionSseCodesSinaService(BaseOptionService):
    """新浪期权合约代码服务"""
    
    collection_name = "option_sse_codes_sina"
    display_name = "新浪期权合约代码"
    unique_fields = ["标的代码", "到期月份", "期权代码"]
    
    async def update_single_data(self, task_id: str = None, trade_date: str = None, underlying: str = None, **kwargs) -> Dict[str, Any]:
        if not trade_date or not underlying:
            return {"success": False, "message": "缺少到期月份(trade_date如202002)或标的代码(underlying如510300)参数"}
        try:
            df = ak.option_sse_codes_sina(trade_date=trade_date, underlying=underlying)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['标的代码'] = underlying
            df['到期月份'] = trade_date
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": "更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        total_count = 0
        for underlying in UNDERLYING_CODES:
            try:
                # 根据标的代码选择对应的品种名称来获取到期月份
                symbol = "50ETF" if underlying == "510050" else "300ETF"
                months = ak.option_sse_list_sina(symbol=symbol, exchange="null")
                for month in months[:2]:  # 最近2个到期月
                    result = await self.update_single_data(trade_date=month, underlying=underlying)
                    if result.get("success"):
                        total_count += result.get("count", 0)
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"获取 {underlying} 合约代码失败: {e}")
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


# 标的物代码列表 (带交易所前缀)
UNDERLYING_SYMBOL_CODES = ["sh510050", "sh510300"]


class OptionSseUnderlyingSpotPriceSinaService(BaseOptionService):
    """期权标的物实时数据服务"""
    
    collection_name = "option_sse_underlying_spot_price_sina"
    display_name = "期权标的物实时数据"
    unique_fields = ["标的代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少标的代码参数（如 sh510300）"}
        try:
            df = ak.option_sse_underlying_spot_price_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['标的代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": "更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        total_count = 0
        for symbol in UNDERLYING_SYMBOL_CODES:
            result = await self.update_single_data(symbol=symbol)
            if result.get("success"):
                total_count += result.get("count", 0)
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionSseGreeksSinaService(BaseOptionService):
    """期权希腊字母服务"""
    
    collection_name = "option_sse_greeks_sina"
    display_name = "期权希腊字母"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_sse_greeks_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": "更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "请使用单条更新，需要指定合约代码"}


class OptionSseMinuteSinaService(BaseOptionService):
    """期权分钟行情服务"""
    
    collection_name = "option_sse_minute_sina"
    display_name = "期权分钟行情"
    unique_fields = ["合约代码", "时间"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_sse_minute_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": "更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "请使用单条更新，需要指定合约代码"}


class OptionSseDailySinaService(BaseOptionService):
    """期权日行情服务"""
    
    collection_name = "option_sse_daily_sina"
    display_name = "期权日行情"
    unique_fields = ["合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_sse_daily_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": "更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "请使用单条更新，需要指定合约代码"}
