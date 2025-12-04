"""
腾讯财经数据提供者

每个交易日 16:00 提供当日数据; 如遇到数据缺失, 请使用 **ak.stock_zh_a_tick_163()** 接口(注意数据会有一定差异)
接口: stock_zh_a_tick_tx
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhATickTxProvider(BaseProvider):
    """腾讯财经数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_tick_tx"
    display_name = "腾讯财经"
    akshare_func = "stock_zh_a_tick_tx"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "每个交易日 16:00 提供当日数据; 如遇到数据缺失, 请使用 **ak.stock_zh_a_tick_163()** 接口(注意数据会有一定差异)"
    collection_route = "/stocks/collections/stock_zh_a_tick_tx"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "成交时间", "type": "object", "description": "-"},
        {"name": "成交价格", "type": "float64", "description": "注意单位: 元"},
        {"name": "价格变动", "type": "float64", "description": "注意单位: 元"},
        {"name": "成交量", "type": "int32", "description": "注意单位: 手"},
        {"name": "成交额", "type": "int32", "description": "注意单位: 元"},
        {"name": "性质", "type": "object", "description": "买卖盘标记"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
