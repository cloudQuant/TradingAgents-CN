"""广期所隐含波动率数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionVolGfexProvider(BaseProvider):
    """广期所隐含波动率数据提供者"""
    
    collection_name = "option_vol_gfex"
    display_name = "广期所隐含波动率"
    akshare_func = "option_vol_gfex"
    unique_keys = ["品种", "合约月份"]
    
    collection_description = "广州期货交易所商品期权数据-隐含波动参考值"
    collection_route = "/options/collections/option_vol_gfex"
    collection_order = 41
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约月份", "type": "string", "description": "合约月份"},
        {"name": "隐含波动率", "type": "float", "description": "隐含波动率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
