"""期货交易费用参照表数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesFeesInfoProvider(SimpleProvider):
    """期货交易费用参照表数据提供者"""
    
    collection_name = "futures_fees_info"
    display_name = "期货交易费用参照表"
    akshare_func = "futures_fees_info"
    unique_keys = ["交易所", "合约代码"]
    
    collection_description = "openctp期货交易费用参照表，包含手续费率、保证金率等信息"
    collection_route = "/futures/collections/futures_fees_info"
    collection_order = 1
    
    field_info = [
        {"name": "交易所", "type": "string", "description": "交易所名称"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "品种代码", "type": "string", "description": "品种代码"},
        {"name": "品种名称", "type": "string", "description": "品种名称"},
        {"name": "合约乘数", "type": "int", "description": "合约乘数"},
        {"name": "最小跳动", "type": "float", "description": "最小变动价位"},
        {"name": "开仓费率（按金额）", "type": "float", "description": ""},
        {"name": "开仓费用（按手）", "type": "float", "description": ""},
        {"name": "平仓费率（按金额）", "type": "float", "description": ""},
        {"name": "平仓费用（按手）", "type": "float", "description": ""},
        {"name": "平今费率（按金额）", "type": "float", "description": ""},
        {"name": "平今费用（按手）", "type": "float", "description": ""},
        {"name": "做多保证金率（按金额）", "type": "float", "description": ""},
        {"name": "做多保证金（按手）", "type": "int", "description": ""},
        {"name": "做空保证金率（按金额）", "type": "float", "description": ""},
        {"name": "做空保证金（按手）", "type": "int", "description": ""},
        {"name": "最新价", "type": "float", "description": "最新价格"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
