"""
股票列表-A股数据提供者

沪深京 A 股股票代码和股票简称数据
接口: stock_info_a_code_name
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockInfoACodeNameProvider(SimpleProvider):
    """股票列表-A股数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_a_code_name"
    display_name = "股票列表-A股"
    akshare_func = "stock_info_a_code_name"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "沪深京 A 股股票代码和股票简称数据"
    collection_route = "/stocks/collections/stock_info_a_code_name"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "code", "type": "object", "description": "-"},
        {"name": "name", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
