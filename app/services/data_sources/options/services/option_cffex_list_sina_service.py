"""
中金所期权合约列表服务 (新浪)
包含: option_cffex_sz50_list_sina, option_cffex_hs300_list_sina, option_cffex_zz1000_list_sina
"""

import akshare as ak
from typing import Dict, Any
import logging

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)


class OptionCffexSz50ListSinaService(BaseOptionService):
    """中金所上证50期权合约列表服务"""
    
    collection_name = "option_cffex_sz50_list_sina"
    display_name = "中金所上证50期权合约"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取中金所上证50期权合约...")
            
            df = ak.option_cffex_sz50_list_sina()
            
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            # 处理DataFrame - 可能是Series或单列
            if isinstance(df, list):
                records = [{"合约代码": code} for code in df]
            else:
                records = df.to_dict('records') if hasattr(df, 'to_dict') else [{"合约代码": str(df)}]
            
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新中金所上证50期权合约失败: {e}")
            return {"success": False, "message": str(e)}


class OptionCffexHs300ListSinaService(BaseOptionService):
    """中金所沪深300期权合约列表服务"""
    
    collection_name = "option_cffex_hs300_list_sina"
    display_name = "中金所沪深300期权合约"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取中金所沪深300期权合约...")
            
            df = ak.option_cffex_hs300_list_sina()
            
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            if isinstance(df, list):
                records = [{"合约代码": code} for code in df]
            else:
                records = df.to_dict('records') if hasattr(df, 'to_dict') else [{"合约代码": str(df)}]
            
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新中金所沪深300期权合约失败: {e}")
            return {"success": False, "message": str(e)}


class OptionCffexZz1000ListSinaService(BaseOptionService):
    """中金所中证1000期权合约列表服务"""
    
    collection_name = "option_cffex_zz1000_list_sina"
    display_name = "中金所中证1000期权合约"
    unique_fields = ["合约代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取中金所中证1000期权合约...")
            
            df = ak.option_cffex_zz1000_list_sina()
            
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            if isinstance(df, list):
                records = [{"合约代码": code} for code in df]
            else:
                records = df.to_dict('records') if hasattr(df, 'to_dict') else [{"合约代码": str(df)}]
            
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新中金所中证1000期权合约失败: {e}")
            return {"success": False, "message": str(e)}
