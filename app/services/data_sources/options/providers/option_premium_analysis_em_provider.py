"""期权折溢价数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionPremiumAnalysisEmProvider(BaseProvider):
    """期权折溢价数据提供者"""
    
    collection_name = "option_premium_analysis_em"
    display_name = "期权折溢价"
    akshare_func = "option_premium_analysis_em"
    unique_keys = ["品种", "合约代码"]
    
    collection_description = "东方财富网-数据中心-特色数据-期权折溢价"
    collection_route = "/options/collections/option_premium_analysis_em"
    collection_order = 31
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "折溢价", "type": "float", "description": "折溢价"},
        {"name": "折溢价率", "type": "float", "description": "折溢价率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
