"""
基金净值估算-东财服务（重构版：继承SimpleService，无参数接口）
"""
import asyncio
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_value_estimation_em_provider import FundValueEstimationEmProvider


class FundValueEstimationEmService(SimpleService):
    """基金净值估算-东财服务（无参数接口，直接获取全部数据）"""
    
    collection_name = "fund_value_estimation_em"
    provider_class = FundValueEstimationEmProvider
    
    # 唯一键配置（基金代码 + 交易日）
    unique_keys = ["基金代码", "交易日"]
    
    # 并发控制锁（防止并发更新）
    _update_lock = asyncio.Lock()
    
    async def update_single_data(self, **kwargs) -> dict:
        """
        更新单条数据（无参数接口，直接获取全部数据）
        """
        async with self._update_lock:
            return await super().update_single_data(**kwargs)
    
    async def update_batch_data(self, **kwargs) -> dict:
        """
        批量更新（无参数接口，直接调用单条更新）
        """
        return await self.update_single_data(**kwargs)
