"""
期权杂项数据服务
包含: option_contract_info_ctp, option_comm_info, option_margin, option_vol_gfex
"""

import akshare as ak
from typing import Dict, Any
from datetime import datetime
import logging

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)


class OptionContractInfoCtpService(BaseOptionService):
    """OpenCTP期权合约信息服务"""
    
    collection_name = "option_contract_info_ctp"
    display_name = "OpenCTP期权合约信息"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取OpenCTP期权合约信息...")
            
            df = ak.option_contract_info_ctp()
            
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
            logger.error(f"更新OpenCTP期权合约信息失败: {e}")
            return {"success": False, "message": str(e)}


class OptionCommInfoService(BaseOptionService):
    """商品期权手续费服务"""
    
    collection_name = "option_comm_info"
    display_name = "商品期权手续费"
    unique_fields = ["品种"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取商品期权手续费...")
            
            df = ak.option_comm_info()
            
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
            logger.error(f"更新商品期权手续费失败: {e}")
            return {"success": False, "message": str(e)}


class OptionMarginService(BaseOptionService):
    """期权保证金服务"""
    
    collection_name = "option_margin"
    display_name = "期权保证金"
    unique_fields = ["品种"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取期权保证金...")
            
            df = ak.option_margin()
            
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
            logger.error(f"更新期权保证金失败: {e}")
            return {"success": False, "message": str(e)}


class OptionVolGfexService(BaseOptionService):
    """广期所隐含波动率服务"""
    
    collection_name = "option_vol_gfex"
    display_name = "广期所隐含波动率"
    unique_fields = ["品种", "日期"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取广期所隐含波动率...")
            
            df = ak.option_vol_gfex()
            
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
            logger.error(f"更新广期所隐含波动率失败: {e}")
            return {"success": False, "message": str(e)}
