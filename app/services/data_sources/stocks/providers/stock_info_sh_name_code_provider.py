"""
股票列表-上证数据提供者

上海证券交易所股票代码和简称数据
接口: stock_info_sh_name_code
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInfoShNameCodeProvider(BaseProvider):
    """股票列表-上证数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_sh_name_code"
    display_name = "股票列表-上证"
    akshare_func = "stock_info_sh_name_code"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "上海证券交易所股票代码和简称数据"
    collection_route = "/stocks/collections/stock_info_sh_name_code"
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
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "公司全称", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
