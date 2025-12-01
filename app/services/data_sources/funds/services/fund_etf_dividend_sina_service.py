"""
基金累计分红-新浪服务（重构版：继承BaseService）
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.fund_etf_dividend_sina_provider import FundEtfDividendSinaProvider


class FundEtfDividendSinaService(BaseService):
    """基金累计分红-新浪服务"""
    
    collection_name = "fund_etf_dividend_sina"
    provider_class = FundEtfDividendSinaProvider
    
    # 批量更新配置：从 fund_spot_sina 获取基金代码列表
    batch_source_collection = "fund_spot_sina"
    batch_source_field = "代码"
    batch_concurrency = 5
    batch_progress_interval = 20
    
    # 增量更新：根据代码和日期检查是否已存在
    incremental_check_fields = ["代码", "日期"]
    
    # 唯一键配置
    unique_keys = ["代码", "日期"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_etf_dividend_sina",
    }
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量更新参数
        
        Args:
            args[0]: 基金代码（如 sh510050）
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 1 and args[0]:
            code = args[0]
            return {"symbol": code}
        raise ValueError(f"get_batch_params 缺少必需的基金代码参数，args={args}")
