"""openctp期权合约信息数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionContractInfoCtpProvider(SimpleProvider):
    """openctp期权合约信息数据提供者"""
    
    collection_name = "option_contract_info_ctp"
    display_name = "openctp期权合约信息"
    akshare_func = "option_contract_info_ctp"
    unique_keys = ["交易所ID", "合约ID"]
    
    collection_description = "openctp期权合约信息"
    collection_route = "/options/collections/option_contract_info_ctp"
    collection_order = 1
    
    field_info = [
        {"name": "交易所ID", "type": "string", "description": "交易所ID"},
        {"name": "合约ID", "type": "string", "description": "合约ID"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "商品类别", "type": "string", "description": "商品类别"},
        {"name": "品种ID", "type": "string", "description": "品种ID"},
        {"name": "合约乘数", "type": "int", "description": "合约乘数"},
        {"name": "最小变动价位", "type": "float", "description": "最小变动价位"},
        {"name": "做多保证金率", "type": "float", "description": "做多保证金率"},
        {"name": "做空保证金率", "type": "float", "description": "做空保证金率"},
        {"name": "做多保证金/手", "type": "float", "description": "做多保证金/手"},
        {"name": "做空保证金/手", "type": "float", "description": "做空保证金/手"},
        {"name": "开仓手续费率", "type": "float", "description": "开仓手续费率"},
        {"name": "开仓手续费/手", "type": "float", "description": "开仓手续费/手"},
        {"name": "平仓手续费率", "type": "float", "description": "平仓手续费率"},
        {"name": "平仓手续费/手", "type": "float", "description": "平仓手续费/手"},
        {"name": "平今手续费率", "type": "float", "description": "平今手续费率"},
        {"name": "平今手续费/手", "type": "float", "description": "平今手续费/手"},
        {"name": "交割年份", "type": "int", "description": "交割年份"},
        {"name": "交割月份", "type": "int", "description": "交割月份"},
        {"name": "上市日期", "type": "string", "description": "上市日期"},
        {"name": "最后交易日", "type": "string", "description": "最后交易日"},
        {"name": "交割日", "type": "string", "description": "交割日"},
        {"name": "标的合约ID", "type": "string", "description": "标的合约ID"},
        {"name": "标的合约乘数", "type": "int", "description": "标的合约乘数"},
        {"name": "期权类型", "type": "string", "description": "期权类型"},
        {"name": "行权价", "type": "float", "description": "行权价"},
        {"name": "合约状态", "type": "string", "description": "合约状态"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
