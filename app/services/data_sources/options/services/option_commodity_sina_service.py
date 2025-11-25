"""
商品期权数据服务 (新浪)
包含: option_commodity_contract_sina, option_commodity_contract_table_sina, option_commodity_hist_sina
"""

import akshare as ak
from typing import Dict, Any
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)

# 商品期权品种列表
COMMODITY_SYMBOLS = ["豆粕期权", "玉米期权", "棕榈油期权", "铁矿石期权", "黄金期权", "铜期权", "白糖期权", "棉花期权"]


class OptionCommodityContractSinaService(BaseOptionService):
    """商品期权在交易合约服务"""
    
    collection_name = "option_commodity_contract_sina"
    display_name = "商品期权在交易合约"
    unique_fields = ["品种", "合约代码"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少品种参数"}
        try:
            df = ak.option_commodity_contract_sina(symbol=symbol)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        total_count = 0
        for i, symbol in enumerate(COMMODITY_SYMBOLS):
            if self.task_manager and task_id:
                progress = int((i / len(COMMODITY_SYMBOLS)) * 90) + 5
                await self.task_manager.update_task(task_id, progress=progress, message=f"更新 {symbol}...")
            
            try:
                result = await self.update_single_data(symbol=symbol)
                if result.get("success"):
                    total_count += result.get("count", 0)
            except Exception as e:
                logger.warning(f"更新 {symbol} 失败: {e}")
            await asyncio.sleep(0.2)
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionCommodityContractTableSinaService(BaseOptionService):
    """商品期权T型报价表服务"""
    
    collection_name = "option_commodity_contract_table_sina"
    display_name = "商品期权T型报价表"
    unique_fields = ["品种", "合约月份", "行权价"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, contract: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol or not contract:
            return {"success": False, "message": "缺少品种或合约月份参数"}
        try:
            df = ak.option_commodity_contract_table_sina(symbol=symbol, contract=contract)
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['品种'] = symbol
            df['合约月份'] = contract
            records = df.to_dict('records')
            result = await self._save_data(records)
            return {"success": True, "message": f"更新完成，{len(records)} 条", "count": len(records)}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        total_count = 0
        completed = 0
        
        for symbol in COMMODITY_SYMBOLS[:4]:  # 限制品种数量
            try:
                # 获取该品种的在交易合约
                contracts_df = ak.option_commodity_contract_sina(symbol=symbol)
                if contracts_df.empty:
                    continue
                
                contracts = contracts_df.iloc[:, 0].tolist()[:3]  # 取前3个合约
                
                for contract in contracts:
                    if self.task_manager and task_id:
                        await self.task_manager.update_task(
                            task_id, progress=min(95, completed * 5 + 5),
                            message=f"更新 {symbol} {contract}..."
                        )
                    
                    result = await self.update_single_data(symbol=symbol, contract=contract)
                    if result.get("success"):
                        total_count += result.get("count", 0)
                    
                    completed += 1
                    await asyncio.sleep(0.2)
            except Exception as e:
                logger.warning(f"更新 {symbol} T型报价失败: {e}")
        
        return {"success": True, "message": f"批量更新完成，共 {total_count} 条", "count": total_count}


class OptionCommodityHistSinaService(BaseOptionService):
    """商品期权历史行情服务"""
    
    collection_name = "option_commodity_hist_sina"
    display_name = "商品期权历史行情"
    unique_fields = ["合约代码", "日期"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        try:
            df = ak.option_commodity_hist_sina(symbol=symbol)
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
