"""
十大股东(个股)数据提供者

东方财富网-个股-十大股东
接口: stock_gdfx_top_10_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGdfxTop10EmProvider(BaseProvider):
    """十大股东(个股)数据提供者"""
    
    # 必填属性
    collection_name = "stock_gdfx_top_10_em"
    display_name = "十大股东(个股)"
    akshare_func = "stock_gdfx_top_10_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-个股-十大股东"
    collection_route = "/stocks/collections/stock_gdfx_top_10_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "名次", "type": "int64", "description": "-"},
        {"name": "股份类型", "type": "object", "description": "-"},
        {"name": "持股数", "type": "int64", "description": "注意单位: 股"},
        {"name": "占总股本持股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "增减", "type": "object", "description": "注意单位: 股"},
        {"name": "变动比率", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
