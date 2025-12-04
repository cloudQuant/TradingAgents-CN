"""
A 股股息率数据提供者

乐咕乐股-股息率-A 股股息率
接口: stock_a_gxl_lg
"""
from app.services.data_sources.base_provider import BaseProvider


class StockAGxlLgProvider(BaseProvider):
    """A 股股息率数据提供者"""
    
    # 必填属性
    collection_name = "stock_a_gxl_lg"
    display_name = "A 股股息率"
    akshare_func = "stock_a_gxl_lg"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-股息率-A 股股息率"
    collection_route = "/stocks/collections/stock_a_gxl_lg"
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
        {"name": "股息率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
