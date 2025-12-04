"""
股本结构数据提供者

东方财富-A股数据-股本结构
接口: stock_zh_a_gbjg_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAGbjgEmProvider(BaseProvider):
    """股本结构数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_gbjg_em"
    display_name = "股本结构"
    akshare_func = "stock_zh_a_gbjg_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-A股数据-股本结构"
    collection_route = "/stocks/collections/stock_zh_a_gbjg_em"
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
        {"name": "变更日期", "type": "object", "description": "-"},
        {"name": "总股本", "type": "int64", "description": "-"},
        {"name": "流通受限股份", "type": "float64", "description": "-"},
        {"name": "其他内资持股(受限)", "type": "float64", "description": "-"},
        {"name": "境内法人持股(受限)", "type": "float64", "description": "-"},
        {"name": "境内自然人持股(受限)", "type": "float64", "description": "-"},
        {"name": "已流通股份", "type": "float64", "description": "-"},
        {"name": "已上市流通A股", "type": "int64", "description": "-"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
