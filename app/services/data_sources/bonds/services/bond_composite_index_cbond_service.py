"""
中债综合指数服务（重构版）

数据集合名称: bond_composite_index_cbond
说明: 批量更新时遍历 indicator × period 所有组合，使用并发控制，显示更新进度
"""
import asyncio
from typing import Any, Dict, List, Optional

from app.services.data_sources.base_service import BaseService
from app.utils.task_manager import get_task_manager
from ..providers.bond_composite_index_cbond_provider import BondCompositeIndexCbondProvider


class BondCompositeIndexCbondService(BaseService):
    """中债综合指数服务"""
    
    collection_name = "bond_composite_index_cbond"
    provider_class = BondCompositeIndexCbondProvider
    
    # 所有可选的 indicator 值
    INDICATORS = [
        "全价", "净价", "财富",
        "平均市值法久期", "平均现金流法久期",
        "平均市值法凸性", "平均现金流法凸性",
        "平均现金流法到期收益率", "平均市值法到期收益率",
        "平均基点价值", "平均待偿期", "平均派息率",
        "指数上日总市值",
        "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅",
        "现券结算量"
    ]
    
    # 所有可选的 period 值
    PERIODS = [
        "总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上"
    ]
    
    # 默认并发数
    DEFAULT_CONCURRENCY = 3

    async def update_batch_data(self, **kwargs) -> Dict[str, Any]:
        """
        批量更新：遍历所有 indicator × period 组合，显示更新进度
        
        Args:
            task_id: 任务ID（用于更新进度）
            concurrency: 并发数，默认 3
        """
        task_id: Optional[str] = kwargs.get("task_id")
        concurrency = int(kwargs.get("concurrency", self.DEFAULT_CONCURRENCY))
        concurrency = max(1, min(concurrency, 10))  # 限制在 1-10 之间
        
        task_manager = get_task_manager()
        
        # 生成所有组合
        combinations = [
            {"indicator": indicator, "period": period}
            for indicator in self.INDICATORS
            for period in self.PERIODS
        ]
        total_combinations = len(combinations)
        
        self.logger.info(
            f"开始批量更新 {self.collection_name}，"
            f"共 {len(self.INDICATORS)} 个指标 × {len(self.PERIODS)} 个期限 = "
            f"{total_combinations} 个组合，并发数: {concurrency}"
        )
        
        if task_id:
            task_manager.update_progress(
                task_id, 0, total_combinations, 
                f"开始批量更新，共 {total_combinations} 个组合..."
            )
        
        total_saved = 0
        total_errors = 0
        error_details: List[str] = []
        completed_count = 0
        
        # 使用信号量控制并发
        semaphore = asyncio.Semaphore(concurrency)
        lock = asyncio.Lock()
        
        async def fetch_one(params: Dict[str, str]) -> Dict[str, Any]:
            nonlocal completed_count
            async with semaphore:
                try:
                    result = await self.update_single_data(**params)
                    return {
                        "params": params,
                        "success": True,
                        "saved_count": result.get("saved_count", 0)
                    }
                except Exception as e:
                    self.logger.warning(
                        f"获取 {params['indicator']}/{params['period']} 失败: {e}"
                    )
                    return {
                        "params": params,
                        "success": False,
                        "error": str(e)
                    }
                finally:
                    # 更新进度
                    async with lock:
                        completed_count += 1
                        if task_id:
                            task_manager.update_progress(
                                task_id, completed_count, total_combinations,
                                f"进度: {completed_count}/{total_combinations} "
                                f"({params['indicator']}/{params['period']})"
                            )
        
        # 并发执行所有任务
        tasks = [fetch_one(params) for params in combinations]
        results = await asyncio.gather(*tasks)
        
        # 统计结果
        for result in results:
            if result["success"]:
                total_saved += result.get("saved_count", 0)
            else:
                total_errors += 1
                params = result["params"]
                error_details.append(
                    f"{params['indicator']}/{params['period']}: {result.get('error', 'Unknown')}"
                )
        
        success_count = total_combinations - total_errors
        
        self.logger.info(
            f"批量更新 {self.collection_name} 完成，"
            f"成功: {success_count}/{total_combinations}，"
            f"保存记录数: {total_saved}"
        )
        
        # 完成任务
        if task_id:
            task_manager.complete_task(
                task_id,
                result={
                    "saved": total_saved,
                    "success_count": success_count,
                    "error_count": total_errors
                },
                message=f"批量更新完成: 成功 {success_count}/{total_combinations}，保存 {total_saved} 条"
            )
        
        return {
            "collection_name": self.collection_name,
            "total_combinations": total_combinations,
            "success_count": success_count,
            "error_count": total_errors,
            "saved_count": total_saved,
            "errors": error_details[:10] if error_details else []  # 最多返回10条错误
        }
