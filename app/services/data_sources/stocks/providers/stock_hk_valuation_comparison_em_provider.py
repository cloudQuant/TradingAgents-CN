"""
估值对比数据提供者

东方财富-港股-行业对比-估值对比
接口: stock_hk_valuation_comparison_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkValuationComparisonEmProvider(BaseProvider):
    """估值对比数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_valuation_comparison_em"
    display_name = "估值对比"
    akshare_func = "stock_hk_valuation_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-行业对比-估值对比"
    collection_route = "/stocks/collections/stock_hk_valuation_comparison_em"
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
        {"name": "市盈率-TTM", "type": "float64", "description": "-"},
        {"name": "市盈率-TTM排名", "type": "int64", "description": "-"},
        {"name": "市盈率-LYR", "type": "float64", "description": "-"},
        {"name": "市盈率-LYR排名", "type": "int64", "description": "-"},
        {"name": "市净率-MRQ", "type": "float64", "description": "-"},
        {"name": "市净率-MRQ排名", "type": "int64", "description": "-"},
        {"name": "市净率-LYR", "type": "float64", "description": "-"},
        {"name": "市净率-LYR排名", "type": "int64", "description": "-"},
        {"name": "市销率-TTM", "type": "float64", "description": "-"},
        {"name": "市销率-TTM排名", "type": "int64", "description": "-"},
        {"name": "市销率-LYR", "type": "float64", "description": "-"},
        {"name": "市销率-LYR排名", "type": "int64", "description": "-"},
        {"name": "市现率-TTM", "type": "float64", "description": "-"},
        {"name": "市现率-TTM排名", "type": "int64", "description": "-"},
        {"name": "市现率-LYR", "type": "float64", "description": "-"},
        {"name": "市现率-LYR排名", "type": "int64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
