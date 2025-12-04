"""期权风险分析数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionRiskAnalysisEmProvider(BaseProvider):
    """期权风险分析数据提供者"""
    
    collection_name = "option_risk_analysis_em"
    display_name = "期权风险分析"
    akshare_func = "option_risk_analysis_em"
    unique_keys = ["品种", "合约代码"]
    
    collection_description = "东方财富网-数据中心-特色数据-期权风险分析"
    collection_route = "/options/collections/option_risk_analysis_em"
    collection_order = 30
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "Delta", "type": "float", "description": "Delta值"},
        {"name": "Gamma", "type": "float", "description": "Gamma值"},
        {"name": "Theta", "type": "float", "description": "Theta值"},
        {"name": "Vega", "type": "float", "description": "Vega值"},
        {"name": "Rho", "type": "float", "description": "Rho值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
