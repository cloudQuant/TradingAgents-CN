"""
基金基本信息-雪球服务（重构版：继承BaseService）

批量更新时从 fund_name_em 集合获取基金代码列表，
然后通过 fund_individual_basic_info_xq 接口逐个获取基金详细信息。
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.fund_basic_info_provider import FundBasicInfoProvider


class FundBasicInfoService(BaseService):
    """基金基本信息-雪球服务"""
    
    collection_name = "fund_basic_info"
    provider_class = FundBasicInfoProvider
    
    # 批量更新配置：从 fund_name_em 获取基金代码列表
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    
    # 并发控制
    batch_concurrency = 5
    batch_progress_interval = 20
    
    # 增量更新：根据基金代码检查是否已存在
    incremental_check_fields = ["基金代码"]
    
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
