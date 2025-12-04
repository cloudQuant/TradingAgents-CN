"""现期图数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesSpotSysProvider(BaseProvider):
    """现期图数据提供者"""
    
    collection_name = "futures_spot_sys"
    display_name = "现期图"
    akshare_func = "futures_spot_sys"
    unique_keys = ["日期", "品种", "合约"]
    
    collection_description = "期货现期图数据"
    collection_route = "/futures/collections/futures_spot_sys"
    collection_order = 22
    
    param_mapping = {"symbol": "symbol", "indicator": "indicator"}
    required_params = ["symbol", "indicator"]
    add_param_columns = {"symbol": "品种", "indicator": "合约"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "合约", "type": "string", "description": "合约类型"},
        {"name": "现货价格", "type": "float", "description": "现货价格"},
        {"name": "期货价格", "type": "float", "description": "期货价格"},
        {"name": "基差", "type": "float", "description": "基差"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
