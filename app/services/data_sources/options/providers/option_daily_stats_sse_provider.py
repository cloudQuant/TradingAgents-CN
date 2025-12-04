"""上交所每日统计数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionDailyStatsSseProvider(BaseProvider):
    """上交所每日统计数据提供者"""
    
    collection_name = "option_daily_stats_sse"
    display_name = "上交所每日统计"
    akshare_func = "option_daily_stats_sse"
    unique_keys = ["日期", "合约标的代码"]
    
    collection_description = "上海证券交易所-产品-股票期权-每日统计"
    collection_route = "/options/collections/option_daily_stats_sse"
    collection_order = 6
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "合约标的代码", "type": "string", "description": "合约标的代码"},
        {"name": "合约标的名称", "type": "string", "description": "合约标的名称"},
        {"name": "合约数量", "type": "int", "description": "合约数量"},
        {"name": "总成交额", "type": "int", "description": "总成交额(万元)"},
        {"name": "总成交量", "type": "int", "description": "总成交量(张)"},
        {"name": "认购成交量", "type": "int", "description": "认购成交量(张)"},
        {"name": "认沽成交量", "type": "int", "description": "认沽成交量(张)"},
        {"name": "认沽/认购", "type": "float", "description": "认沽/认购比例(%)"},
        {"name": "未平仓合约总数", "type": "int", "description": "未平仓合约总数"},
        {"name": "未平仓认购合约数", "type": "int", "description": "未平仓认购合约数"},
        {"name": "未平仓认沽合约数", "type": "int", "description": "未平仓认沽合约数"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
