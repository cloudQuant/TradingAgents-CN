"""
破净股统计数据提供者

乐咕乐股-A 股破净股统计数据
接口: stock_a_below_net_asset_statistics
"""
from app.services.data_sources.base_provider import BaseProvider


class StockABelowNetAssetStatisticsProvider(BaseProvider):
    """破净股统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_a_below_net_asset_statistics"
    display_name = "破净股统计"
    akshare_func = "stock_a_below_net_asset_statistics"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-A 股破净股统计数据"
    collection_route = "/stocks/collections/stock_a_below_net_asset_statistics"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "交易日"},
        {"name": "below_net_asset", "type": "float64", "description": "破净股家数"},
        {"name": "total_company", "type": "float64", "description": "总公司数"},
        {"name": "below_net_asset_ratio", "type": "float64", "description": "破净股比率"},
        {"name": "date", "type": "object", "description": "交易日"},
        {"name": "below_net_asset", "type": "float64", "description": "破净股家数"},
        {"name": "total_company", "type": "float64", "description": "总公司数"},
        {"name": "below_net_asset_ratio", "type": "float64", "description": "破净股比率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
