"""
股票列表-深证数据提供者

深证证券交易所股票代码和股票简称数据
接口: stock_info_sz_name_code
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInfoSzNameCodeProvider(BaseProvider):
    """股票列表-深证数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_sz_name_code"
    display_name = "股票列表-深证"
    akshare_func = "stock_info_sz_name_code"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深证证券交易所股票代码和股票简称数据"
    collection_route = "/stocks/collections/stock_info_sz_name_code"
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
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "A股代码", "type": "object", "description": "-"},
        {"name": "A股简称", "type": "object", "description": "-"},
        {"name": "A股上市日期", "type": "object", "description": "-"},
        {"name": "A股总股本", "type": "object", "description": "-"},
        {"name": "A股流通股本", "type": "object", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
