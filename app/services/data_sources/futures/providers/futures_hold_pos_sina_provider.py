"""成交持仓-新浪数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesHoldPosSinaProvider(SimpleProvider):
    """成交持仓-新浪数据提供者"""
    
    collection_name = "futures_hold_pos_sina"
    display_name = "成交持仓-新浪"
    akshare_func = "futures_hold_pos_sina"
    unique_keys = ["日期", "品种", "合约"]
    
    collection_description = "新浪期货成交持仓数据"
    collection_route = "/futures/collections/futures_hold_pos_sina"
    collection_order = 21
    
    field_info = [
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "合约", "type": "string", "description": "合约代码"},
        {"name": "成交量", "type": "float", "description": "成交量"},
        {"name": "持仓量", "type": "float", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
