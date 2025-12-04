"""金融期权股票期权分时行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionFinanceMinuteSinaProvider(BaseProvider):
    """金融期权股票期权分时行情数据提供者"""
    
    collection_name = "option_finance_minute_sina"
    display_name = "金融期权股票期权分时行情"
    akshare_func = "option_finance_minute_sina"
    unique_keys = ["合约代码", "时间"]
    
    collection_description = "新浪财经-金融期权-股票期权-分时行情数据"
    collection_route = "/options/collections/option_finance_minute_sina"
    collection_order = 25
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "时间", "type": "string", "description": "时间"},
        {"name": "价格", "type": "float", "description": "价格"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
