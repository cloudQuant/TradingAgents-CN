"""
估值比较数据提供者

东方财富-行情中心-同行比较-估值比较
接口: stock_zh_valuation_comparison_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhValuationComparisonEmProvider(BaseProvider):
    """估值比较数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_valuation_comparison_em"
    display_name = "估值比较"
    akshare_func = "stock_zh_valuation_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情中心-同行比较-估值比较"
    collection_route = "/stocks/collections/stock_zh_valuation_comparison_em"
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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "PEG", "type": "float64", "description": "-"},
        {"name": "市盈率-24A", "type": "float64", "description": "-"},
        {"name": "市盈率-TTM", "type": "float64", "description": "-"},
        {"name": "市盈率-25E", "type": "float64", "description": "-"},
        {"name": "市盈率-26E", "type": "float64", "description": "-"},
        {"name": "市盈率-27E", "type": "float64", "description": "-"},
        {"name": "市销率-24A", "type": "float64", "description": "-"},
        {"name": "市销率-TTM", "type": "float64", "description": "-"},
        {"name": "市销率-25E", "type": "float64", "description": "-"},
        {"name": "市销率-26E", "type": "float64", "description": "-"},
        {"name": "市销率-27E", "type": "float64", "description": "-"},
        {"name": "市净率-24A", "type": "float64", "description": "-"},
        {"name": "市净率-MRQ", "type": "float64", "description": "-"},
        {"name": "市现率PCE-24A", "type": "float64", "description": "-"},
        {"name": "市现率PCE-TTM", "type": "float64", "description": "-"},
        {"name": "市现率PCF-24A", "type": "float64", "description": "-"},
        {"name": "市现率PCF-TTM", "type": "float64", "description": "-"},
        {"name": "EV/EBITDA-24A", "type": "float64", "description": "-"},
        {"name": "PEG排名", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
