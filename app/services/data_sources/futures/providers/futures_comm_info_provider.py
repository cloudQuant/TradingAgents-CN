"""期货手续费与保证金数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesCommInfoProvider(BaseProvider):
    """期货手续费与保证金数据提供者"""
    
    collection_name = "futures_comm_info"
    display_name = "期货手续费与保证金"
    akshare_func = "futures_comm_info"
    unique_keys = ["交易所名称", "合约代码"]
    
    collection_description = "九期网期货手续费与保证金数据"
    collection_route = "/futures/collections/futures_comm_info"
    collection_order = 2
    
    param_mapping = {
        "symbol": "symbol",
    }
    required_params = []  # symbol有默认值"所有"
    
    field_info = [
        {"name": "交易所名称", "type": "string", "description": ""},
        {"name": "合约名称", "type": "string", "description": ""},
        {"name": "合约代码", "type": "string", "description": ""},
        {"name": "现价", "type": "float", "description": ""},
        {"name": "涨停板", "type": "float", "description": ""},
        {"name": "跌停板", "type": "float", "description": ""},
        {"name": "保证金-买开", "type": "float", "description": "单位: %"},
        {"name": "保证金-卖开", "type": "float", "description": "单位: %"},
        {"name": "保证金-每手", "type": "float", "description": "单位: 元"},
        {"name": "手续费标准-开仓-万分之", "type": "float", "description": ""},
        {"name": "手续费标准-开仓-元", "type": "string", "description": ""},
        {"name": "手续费标准-平昨-万分之", "type": "float", "description": ""},
        {"name": "手续费标准-平昨-元", "type": "string", "description": ""},
        {"name": "手续费标准-平今-万分之", "type": "float", "description": ""},
        {"name": "手续费标准-平今-元", "type": "string", "description": ""},
        {"name": "每跳毛利", "type": "int", "description": "单位: 元"},
        {"name": "手续费", "type": "float", "description": "开+平"},
        {"name": "每跳净利", "type": "float", "description": "单位: 元"},
        {"name": "备注", "type": "string", "description": "是否主力合约"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
