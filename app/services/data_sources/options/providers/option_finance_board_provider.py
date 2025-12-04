"""金融期权行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionFinanceBoardProvider(BaseProvider):
    """金融期权行情数据提供者"""
    
    collection_name = "option_finance_board"
    display_name = "金融期权行情数据"
    akshare_func = "option_finance_board"
    unique_keys = ["日期", "合约交易代码"]
    
    collection_description = "上海证券交易所、深圳证券交易所、中国金融期货交易所的金融期权行情数据"
    collection_route = "/options/collections/option_finance_board"
    collection_order = 2
    
    param_mapping = {"symbol": "symbol", "end_month": "end_month"}
    required_params = ["symbol", "end_month"]
    add_param_columns = {"symbol": "标的品种"}
    
    field_info = [
        {"name": "标的品种", "type": "string", "description": "标的品种名称"},
        {"name": "日期", "type": "string", "description": "日期时间"},
        {"name": "合约交易代码", "type": "string", "description": "合约交易代码"},
        {"name": "当前价", "type": "float", "description": "当前价"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "前结价", "type": "float", "description": "前结价"},
        {"name": "行权价", "type": "float", "description": "行权价"},
        {"name": "数量", "type": "int", "description": "当前总的合约数量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
