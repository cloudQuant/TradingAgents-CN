"""
东方财富期权数据服务
包含: option_current_em, option_lhb_em, option_value_analysis_em, 
      option_risk_analysis_em, option_premium_analysis_em, option_minute_em
"""

import akshare as ak
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import asyncio

from app.services.data_sources.options.services.base_service import BaseOptionService

logger = logging.getLogger(__name__)


class OptionCurrentEmService(BaseOptionService):
    """期权实时数据服务"""
    
    collection_name = "option_current_em"
    display_name = "期权实时数据"
    unique_fields = ["代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """单条更新（此集合不支持）"""
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新期权实时数据"""
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取期权实时数据...")
            
            df = ak.option_current_em()
            
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=50, message="正在保存数据...")
            
            records = df.to_dict('records')
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新期权实时数据失败: {e}")
            return {"success": False, "message": str(e)}


# 龙虎榜标的代码和指标
LHB_SYMBOLS = ["510050", "510300", "159919"]
LHB_INDICATORS = ["期权交易情况-认沽交易量", "期权持仓情况-认沽持仓量", "期权交易情况-认购交易量", "期权持仓情况-认购持仓量"]


class OptionLhbEmService(BaseOptionService):
    """期权龙虎榜服务"""
    
    collection_name = "option_lhb_em"
    display_name = "期权龙虎榜"
    unique_fields = ["证券代码", "交易日期", "交易类型", "机构"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, indicator: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        """单条更新指定标的和指标的龙虎榜数据"""
        if not all([symbol, indicator, trade_date]):
            return {"success": False, "message": "缺少必要参数：symbol(标的代码)、indicator(指标)、trade_date(交易日)"}
        try:
            df = ak.option_lhb_em(symbol=symbol, indicator=indicator, trade_date=trade_date)
            
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
            logger.error(f"更新期权龙虎榜失败: {e}")
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, trade_date: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新所有标的和指标的龙虎榜数据"""
        try:
            if not trade_date:
                trade_date = datetime.now().strftime("%Y%m%d")
            
            total_count = 0
            completed = 0
            total_tasks = len(LHB_SYMBOLS) * len(LHB_INDICATORS)
            
            for symbol in LHB_SYMBOLS:
                for indicator in LHB_INDICATORS:
                    if self.task_manager and task_id:
                        progress = int((completed / total_tasks) * 90) + 5
                        await self.task_manager.update_task(
                            task_id, progress=progress, 
                            message=f"更新 {symbol} {indicator}..."
                        )
                    
                    try:
                        result = await self.update_single_data(
                            symbol=symbol, indicator=indicator, trade_date=trade_date
                        )
                        if result.get("success"):
                            total_count += result.get("count", 0)
                    except Exception as e:
                        logger.warning(f"获取 {symbol} {indicator} 失败: {e}")
                    
                    completed += 1
                    await asyncio.sleep(0.2)
            
            return {
                "success": True,
                "message": f"批量更新完成，共 {total_count} 条",
                "count": total_count
            }
        except Exception as e:
            logger.error(f"批量更新期权龙虎榜失败: {e}")
            return {"success": False, "message": str(e)}


class OptionValueAnalysisEmService(BaseOptionService):
    """期权价值分析服务"""
    
    collection_name = "option_value_analysis_em"
    display_name = "期权价值分析"
    unique_fields = ["代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取期权价值分析...")
            
            df = ak.option_value_analysis_em()
            
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
            logger.error(f"更新期权价值分析失败: {e}")
            return {"success": False, "message": str(e)}


class OptionRiskAnalysisEmService(BaseOptionService):
    """期权风险分析服务"""
    
    collection_name = "option_risk_analysis_em"
    display_name = "期权风险分析"
    unique_fields = ["代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取期权风险分析...")
            
            df = ak.option_risk_analysis_em()
            
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
            logger.error(f"更新期权风险分析失败: {e}")
            return {"success": False, "message": str(e)}


class OptionPremiumAnalysisEmService(BaseOptionService):
    """期权折溢价分析服务"""
    
    collection_name = "option_premium_analysis_em"
    display_name = "期权折溢价"
    unique_fields = ["代码"]
    
    async def update_single_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        return {"success": False, "message": "此集合不支持单条更新"}
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=10, message="正在获取期权折溢价...")
            
            df = ak.option_premium_analysis_em()
            
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
            logger.error(f"更新期权折溢价失败: {e}")
            return {"success": False, "message": str(e)}


class OptionMinuteEmService(BaseOptionService):
    """东财期权分时行情服务"""
    
    collection_name = "option_minute_em"
    display_name = "东财期权分时行情"
    unique_fields = ["代码", "时间"]
    
    async def update_single_data(self, task_id: str = None, symbol: str = None, **kwargs) -> Dict[str, Any]:
        """更新单个合约的分时行情"""
        if not symbol:
            return {"success": False, "message": "缺少合约代码参数"}
        
        try:
            df = ak.option_minute_em(symbol=symbol)
            
            if df.empty:
                return {"success": True, "message": "无数据", "count": 0}
            
            df['代码'] = symbol
            records = df.to_dict('records')
            result = await self._save_data(records)
            
            return {
                "success": True,
                "message": f"更新完成，新增 {result['inserted']} 条，更新 {result['updated']} 条",
                "count": len(records)
            }
        except Exception as e:
            logger.error(f"更新期权分时行情失败: {e}")
            return {"success": False, "message": str(e)}
    
    async def update_batch_data(self, task_id: str = None, concurrency: int = 3, **kwargs) -> Dict[str, Any]:
        """批量更新所有合约的分时行情"""
        try:
            if self.task_manager and task_id:
                await self.task_manager.update_task(task_id, progress=5, message="正在获取合约列表...")
            
            # 先获取当前期权列表
            current_df = ak.option_current_em()
            if current_df.empty:
                return {"success": True, "message": "无期权合约", "count": 0}
            
            symbols = current_df['代码'].tolist()[:50]  # 限制数量避免过多请求
            total = len(symbols)
            completed = 0
            total_count = 0
            
            semaphore = asyncio.Semaphore(concurrency)
            
            async def fetch_one(symbol):
                nonlocal completed, total_count
                async with semaphore:
                    try:
                        result = await self.update_single_data(symbol=symbol)
                        if result.get("success"):
                            total_count += result.get("count", 0)
                    except Exception as e:
                        logger.warning(f"获取 {symbol} 分时数据失败: {e}")
                    
                    completed += 1
                    if self.task_manager and task_id:
                        progress = int((completed / total) * 90) + 5
                        await self.task_manager.update_task(
                            task_id, 
                            progress=progress,
                            message=f"已处理 {completed}/{total} 个合约"
                        )
                    
                    await asyncio.sleep(0.1)  # 限流
            
            await asyncio.gather(*[fetch_one(s) for s in symbols])
            
            return {
                "success": True,
                "message": f"批量更新完成，共处理 {total} 个合约，{total_count} 条数据",
                "count": total_count
            }
        except Exception as e:
            logger.error(f"批量更新期权分时行情失败: {e}")
            return {"success": False, "message": str(e)}
