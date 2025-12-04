"""深交所当日合约数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionCurrentDaySzseProvider(SimpleProvider):
    """深交所当日合约数据提供者"""
    
    collection_name = "option_current_day_szse"
    display_name = "深交所当日合约"
    akshare_func = "option_current_day_szse"
    unique_keys = ["合约编码"]
    
    collection_description = "深圳证券交易所-期权子网-行情数据-当日合约"
    collection_route = "/options/collections/option_current_day_szse"
    collection_order = 5
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "合约编码", "type": "int", "description": "合约编码"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约简称", "type": "string", "description": "合约简称"},
        {"name": "标的证券简称(代码)", "type": "string", "description": "标的证券简称(代码)"},
        {"name": "合约类型", "type": "string", "description": "合约类型"},
        {"name": "行权价", "type": "float", "description": "行权价"},
        {"name": "合约单位", "type": "int", "description": "合约单位"},
        {"name": "最后交易日", "type": "string", "description": "最后交易日"},
        {"name": "行权日", "type": "string", "description": "行权日"},
        {"name": "到期日", "type": "string", "description": "到期日"},
        {"name": "交收日", "type": "string", "description": "交收日"},
        {"name": "新挂", "type": "string", "description": "新挂"},
        {"name": "涨停价格", "type": "float", "description": "涨停价格"},
        {"name": "跌停价格", "type": "float", "description": "跌停价格"},
        {"name": "前结算价", "type": "float", "description": "前结算价"},
        {"name": "交易日期", "type": "string", "description": "交易日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
