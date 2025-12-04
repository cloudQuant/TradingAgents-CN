"""生猪-核心数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesHogCoreProvider(BaseProvider):
    """生猪-核心数据提供者"""
    
    collection_name = "futures_hog_core"
    display_name = "生猪-核心数据"
    akshare_func = "futures_hog_core"
    unique_keys = ["区域", "日期"]
    
    collection_description = "生猪核心数据"
    collection_route = "/futures/collections/futures_hog_core"
    collection_order = 48
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "区域"}
    
    field_info = [
        {"name": "区域", "type": "string", "description": "区域代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "价格", "type": "float", "description": "价格"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
