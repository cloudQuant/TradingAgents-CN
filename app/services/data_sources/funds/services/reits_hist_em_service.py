"""
REITs历史行情-东财服务（重构版：继承BaseService，需要symbol参数）
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.reits_hist_em_provider import ReitsHistEmProvider


class ReitsHistEmService(BaseService):
    """REITs历史行情-东财服务（需要基金代码参数）"""
    
    collection_name = "reits_hist_em"
    provider_class = ReitsHistEmProvider
    
    # 批量更新配置：从 reits_realtime_em 获取基金代码列表
    batch_source_collection = "reits_realtime_em"
    batch_source_field = "代码"
    
    # 并发控制
    batch_concurrency = 3
    batch_progress_interval = 20
    
    # 增量更新：根据基金代码检查是否已存在（历史数据会不断更新，所以只检查基金代码）
    incremental_check_fields = ["基金代码"]
    
    # 唯一键配置（基金代码 + 日期）
    unique_keys = ["基金代码", "日期"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "reits_hist_em",
    }
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量更新参数
        
        Args:
            args[0]: REITs代码
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 1 and args[0]:
            code = args[0]
            return {"symbol": code}
        raise ValueError(f"get_batch_params 缺少必需的REITs代码参数，args={args}")
