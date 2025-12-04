"""商品期权历史行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionCommodityHistSinaProvider(BaseProvider):
    """商品期权历史行情数据提供者"""
    
    collection_name = "option_commodity_hist_sina"
    display_name = "商品期权历史行情"
    akshare_func = "option_commodity_hist_sina"
    unique_keys = ["合约代码", "日期"]
    
    collection_description = "新浪财经-商品期权的历史行情数据-日频率"
    collection_route = "/options/collections/option_commodity_hist_sina"
    collection_order = 34
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
