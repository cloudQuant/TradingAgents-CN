"""生猪-成本维度提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesHogCostProvider(BaseProvider):
    """生猪-成本维度提供者"""
    
    collection_name = "futures_hog_cost"
    display_name = "生猪-成本维度"
    akshare_func = "futures_hog_cost"
    unique_keys = ["区域", "日期"]
    
    collection_description = "生猪成本维度数据"
    collection_route = "/futures/collections/futures_hog_cost"
    collection_order = 49
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "区域"}
    
    field_info = [
        {"name": "区域", "type": "string", "description": "区域代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "成本", "type": "float", "description": "成本"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
