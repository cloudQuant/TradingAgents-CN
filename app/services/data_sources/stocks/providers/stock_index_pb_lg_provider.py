"""
指数市净率数据提供者

乐咕乐股-指数市净率
接口: stock_index_pb_lg
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndexPbLgProvider(BaseProvider):
    """指数市净率数据提供者"""
    
    # 必填属性
    collection_name = "stock_index_pb_lg"
    display_name = "指数市净率"
    akshare_func = "stock_index_pb_lg"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-指数市净率"
    collection_route = "/stocks/collections/stock_index_pb_lg"
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
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "指数", "type": "float64", "description": "-"},
        {"name": "市净率", "type": "float64", "description": "-"},
        {"name": "等权市净率", "type": "float64", "description": "-"},
        {"name": "市净率中位数", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
