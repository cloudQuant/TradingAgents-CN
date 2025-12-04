"""中金所沪深300指数实时行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionCffexHs300SpotSinaProvider(BaseProvider):
    """中金所沪深300指数实时行情数据提供者"""
    
    collection_name = "option_cffex_hs300_spot_sina"
    display_name = "中金所沪深300指数实时行情"
    akshare_func = "option_cffex_hs300_spot_sina"
    unique_keys = ["symbol", "时间"]
    
    collection_description = "新浪财经-中金所沪深300指数指定合约实时行情"
    collection_route = "/options/collections/option_cffex_hs300_spot_sina"
    collection_order = 12
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "时间", "type": "string", "description": "时间"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
