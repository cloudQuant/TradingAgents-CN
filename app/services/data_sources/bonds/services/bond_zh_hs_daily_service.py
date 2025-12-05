"""
沪深债券历史行情服务（重构版）

需求文档: tests/bonds/requirements/04_沪深债券历史行情.md
数据唯一标识: 债券代码和日期

增量更新逻辑：
1. 从 bond_zh_hs_spot 集合获取所有债券代码
2. 从当前 bond_zh_hs_daily 集合获取已有的债券代码
3. 过滤出需要更新的代码（增量）
4. 遍历这些代码调用 update_single_data
"""
from typing import Dict, Any

from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_hs_daily_provider import BondZhHsDailyProvider


class BondZhHsDailyService(BaseService):
    """沪深债券历史行情服务"""
    
    collection_name = "bond_zh_hs_daily"
    provider_class = BondZhHsDailyProvider
    
    # ===== 批量更新配置 =====
    # 从 bond_zh_hs_spot 集合获取债券代码列表
    batch_source_collection = "bond_zh_hs_spot"
    batch_source_field = "代码"  # 源集合中的代码字段名
    
    # 增量更新：检查 bond_zh_hs_daily 中已存在的债券代码
    incremental_check_fields = ["债券代码"]
    
    # 批量更新配置
    batch_concurrency = 3  # 默认并发数
    batch_task_timeout = 120  # 单个任务超时时间（秒）
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        根据任务参数构建 provider 调用参数
        
        Args:
            args[0]: 债券代码（从 bond_zh_hs_spot 的"代码"字段获取）
            
        Returns:
            provider 调用参数，如 {"symbol": "sh010107"}
        """
        if len(args) >= 1:
            return {"symbol": args[0]}
        return {}
