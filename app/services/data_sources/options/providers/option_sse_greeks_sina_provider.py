"""期权希腊字母信息表数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionSseGreeksSinaProvider(BaseProvider):
    """期权希腊字母信息表数据提供者"""
    
    collection_name = "option_sse_greeks_sina"
    display_name = "期权希腊字母信息表"
    akshare_func = "option_sse_greeks_sina"
    unique_keys = ["合约代码"]
    
    collection_description = "新浪财经-期权希腊字母信息表"
    collection_route = "/options/collections/option_sse_greeks_sina"
    collection_order = 22
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "Delta", "type": "float", "description": "Delta值"},
        {"name": "Gamma", "type": "float", "description": "Gamma值"},
        {"name": "Theta", "type": "float", "description": "Theta值"},
        {"name": "Vega", "type": "float", "description": "Vega值"},
        {"name": "Rho", "type": "float", "description": "Rho值"},
        {"name": "隐含波动率", "type": "float", "description": "隐含波动率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
