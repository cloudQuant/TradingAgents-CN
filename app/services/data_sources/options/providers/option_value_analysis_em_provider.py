"""期权价值分析数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionValueAnalysisEmProvider(BaseProvider):
    """期权价值分析数据提供者"""
    
    collection_name = "option_value_analysis_em"
    display_name = "期权价值分析"
    akshare_func = "option_value_analysis_em"
    unique_keys = ["品种", "合约代码"]
    
    collection_description = "东方财富网-数据中心-特色数据-期权价值分析"
    collection_route = "/options/collections/option_value_analysis_em"
    collection_order = 29
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "内在价值", "type": "float", "description": "内在价值"},
        {"name": "时间价值", "type": "float", "description": "时间价值"},
        {"name": "理论价值", "type": "float", "description": "理论价值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
