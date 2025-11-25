"""
中金所期权行情服务 (新浪)
包含: option_cffex_sz50_spot_sina, option_cffex_hs300_spot_sina, option_cffex_zz1000_spot_sina
      option_cffex_sz50_daily_sina, option_cffex_hs300_daily_sina, option_cffex_zz1000_daily_sina
"""

import akshare as ak
from typing import Dict, Any
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)


class OptionCffexSz50SpotSinaService(BaseOptionService):
    """中金所上证50指数期权实时行情服务"""
    
    collection_name = "option_cffex_sz50_spot_sina"
    display_name = "中金所上证50指数实时行情"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_cffex_sz50_spot_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            # 获取合约列表
            contracts = ak.option_cffex_sz50_list_sina()
            if not contracts:
                return {"success": True, "message": "无合约", "count": 0}
            
            total_count = 0
            for i, symbol in enumerate(contracts[:20]):  # 限制数量
                if self.task_manager and task_id:
                    progress = int((i / len(contracts[:20])) * 90) + 5
                    await self.task_manager.update_task(task_id, progress=progress, message=f"更新 {symbol}...")
                
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.1)
            
            return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
        except Exception as e:
            return {"success": False, "message": str(e)}


class OptionCffexHs300SpotSinaService(BaseOptionService):
    """中金所沪深300指数期权实时行情服务"""
    
    collection_name = "option_cffex_hs300_spot_sina"
    display_name = "中金所沪深300指数实时行情"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_cffex_hs300_spot_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            contracts = ak.option_cffex_hs300_list_sina()
            if not contracts:
                return {"success": True, "message": "无合约", "count": 0}
            
            total_count = 0
            for i, symbol in enumerate(contracts[:20]):
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, progress=int((i/20)*90)+5, message=f"更新 {symbol}...")
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.1)
            
            return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
        except Exception as e:
            return {"success": False, "message": str(e)}


class OptionCffexZz1000SpotSinaService(BaseOptionService):
    """中金所中证1000指数期权实时行情服务"""
    
    collection_name = "option_cffex_zz1000_spot_sina"
    display_name = "中金所中证1000指数实时行情"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_cffex_zz1000_spot_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            contracts = ak.option_cffex_zz1000_list_sina()
            if not contracts:
                return {"success": True, "message": "无合约", "count": 0}
            
            total_count = 0
            for i, symbol in enumerate(contracts[:20]):
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, progress=int((i/20)*90)+5, message=f"更新 {symbol}...")
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.1)
            
            return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
        except Exception as e:
            return {"success": False, "message": str(e)}


class OptionCffexSz50DailySinaService(BaseOptionService):
    """中金所上证50指数期权日频行情服务"""
    
    collection_name = "option_cffex_sz50_daily_sina"
    display_name = "中金所上证50指数日频行情"
    unique_fields = ["合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_cffex_sz50_daily_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            contracts = ak.option_cffex_sz50_list_sina()
            if not contracts:
                return {"success": True, "message": "无合约", "count": 0}
            
            total_count = 0
            for i, symbol in enumerate(contracts[:10]):
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, progress=int((i/10)*90)+5, message=f"更新 {symbol}...")
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
            
            return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
        except Exception as e:
            return {"success": False, "message": str(e)}


class OptionCffexHs300DailySinaService(BaseOptionService):
    """中金所沪深300指数期权日频行情服务"""
    
    collection_name = "option_cffex_hs300_daily_sina"
    display_name = "中金所沪深300指数日频行情"
    unique_fields = ["合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_cffex_hs300_daily_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            contracts = ak.option_cffex_hs300_list_sina()
            if not contracts:
                return {"success": True, "message": "无合约", "count": 0}
            
            total_count = 0
            for i, symbol in enumerate(contracts[:10]):
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, progress=int((i/10)*90)+5, message=f"更新 {symbol}...")
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
            
            return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
        except Exception as e:
            return {"success": False, "message": str(e)}


class OptionCffexZz1000DailySinaService(BaseOptionService):
    """中金所中证1000指数期权日频行情服务"""
    
    collection_name = "option_cffex_zz1000_daily_sina"
    display_name = "中金所中证1000指数日频行情"
    unique_fields = ["合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_cffex_zz1000_daily_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            df['合约代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            contracts = ak.option_cffex_zz1000_list_sina()
            if not contracts:
                return {"success": True, "message": "无合约", "count": 0}
            
            total_count = 0
            for i, symbol in enumerate(contracts[:10]):
                if self.task_manager and task_id:
                    await self.task_manager.update_task(task_id, progress=int((i/10)*90)+5, message=f"更新 {symbol}...")
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
                await asyncio.sleep(0.2)
            
            return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}
        except Exception as e:
            return {"success": False, "message": str(e)}
