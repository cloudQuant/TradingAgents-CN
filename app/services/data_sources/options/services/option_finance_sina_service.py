"""
金融期权数据服务 (新浪)
包含: option_finance_minute_sina
"""

import akshare as ak
from typing import Dict, Any
import logging

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)


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
