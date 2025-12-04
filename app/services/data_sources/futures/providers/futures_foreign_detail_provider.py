"""外盘-合约详情提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesForeignDetailProvider(BaseProvider):
    """外盘-合约详情提供者"""
    
    collection_name = "futures_foreign_detail"
    display_name = "外盘-合约详情"
    akshare_func = "futures_foreign_detail"
    unique_keys = ["symbol"]
    
    collection_description = "外盘期货合约详情"
    collection_route = "/futures/collections/futures_foreign_detail"
    collection_order = 40
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "交易所", "type": "string", "description": "交易所"},
        {"name": "合约单位", "type": "string", "description": "合约单位"},
        {"name": "最小变动", "type": "string", "description": "最小变动"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
