"""
基金盈利概率-雪球服务（重构版：继承BaseService，需要symbol参数）
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.fund_individual_profit_probability_xq_provider import FundIndividualProfitProbabilityXqProvider


class FundIndividualProfitProbabilityXqService(BaseService):
    """基金盈利概率-雪球服务（需要基金代码参数）"""
    
    collection_name = "fund_individual_profit_probability_xq"
    provider_class = FundIndividualProfitProbabilityXqProvider
    
    # 批量更新配置：从 fund_name_em 获取基金代码列表
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    
    # 并发控制
    batch_concurrency = 3
    batch_progress_interval = 20
    
    # 增量更新：根据基金代码检查是否已存在
    incremental_check_fields = ["基金代码"]
    
    # 唯一键配置（基金代码 + 持有时长 + 更新时间）
    unique_keys = ["基金代码", "持有时长", "更新时间"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_individual_profit_probability_xq",
    }
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量更新参数
        
        Args:
            args[0]: 基金代码
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 1 and args[0]:
            code = args[0]
            return {"symbol": code}
        raise ValueError(f"get_batch_params 缺少必需的基金代码参数，args={args}")
