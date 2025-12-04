"""
股票列表-北证数据提供者

北京证券交易所股票代码和简称数据
接口: stock_info_bj_name_code
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockInfoBjNameCodeProvider(SimpleProvider):
    """股票列表-北证数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_bj_name_code"
    display_name = "股票列表-北证"
    akshare_func = "stock_info_bj_name_code"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "北京证券交易所股票代码和简称数据"
    collection_route = "/stocks/collections/stock_info_bj_name_code"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "总股本", "type": "int64", "description": "注意单位: 股"},
        {"name": "流通股本", "type": "int64", "description": "注意单位: 股"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "地区", "type": "object", "description": "-"},
        {"name": "报告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
