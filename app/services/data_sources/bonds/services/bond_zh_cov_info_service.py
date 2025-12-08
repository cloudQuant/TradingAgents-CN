"""
可转债详情-东财服务（重构版）

数据集合名称: bond_zh_cov_info
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_cov_info_provider import BondZhCovInfoProvider


class BondZhCovInfoService(BaseService):
    """可转债详情-东财服务"""
    
    collection_name = "bond_zh_cov_info"
    provider_class = BondZhCovInfoProvider

    # 批量更新配置：从可转债数据一览表中获取债券代码列表
    batch_source_collection = "bond_zh_cov"
    batch_source_field = "债券代码"
    batch_concurrency = 3

    # 增量更新配置：按 (债券代码, 指标类型) 组合去重
    incremental_check_fields = ["债券代码", "指标类型"]

    # 支持的指标类型列表（当前仅保留"基本信息"）
    INDICATORS = ["基本信息"]

    async def _get_tasks_to_process(self, codes, years):
        """生成需要处理的 (债券代码, 指标类型) 任务列表（增量）。

        - 从源集合获取到的 codes 为债券代码
        - 对每个债券代码，尝试 4 个指标类型
        - 已存在于 bond_zh_cov_info 中的 (债券代码, 指标类型) 组合将被跳过
        """
        # 获取已存在的 (债券代码, 指标类型) 组合
        existing = await self._get_existing_combinations() if self.incremental_check_fields else set()

        tasks = []
        if not codes:
            return tasks

        for code in codes:
            code_str = str(code)
            for indicator in self.INDICATORS:
                key = (code_str, indicator)
                if existing and key in existing:
                    # 已存在该组合，跳过
                    continue
                tasks.append((code_str, indicator))

        return tasks

    def get_batch_params(self, bond_code, indicator):
        """根据债券代码和指标类型构造 Provider 调用参数。"""
        if not bond_code:
            return {}
        return {"symbol": str(bond_code), "indicator": indicator}
