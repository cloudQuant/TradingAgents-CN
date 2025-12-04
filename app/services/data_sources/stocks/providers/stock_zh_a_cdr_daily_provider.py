"""
历史行情数据数据提供者

上海证券交易所-科创板-CDR
接口: stock_zh_a_cdr_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhACdrDailyProvider(BaseProvider):
    """历史行情数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_cdr_daily"
    display_name = "历史行情数据"
    akshare_func = "stock_zh_a_cdr_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "上海证券交易所-科创板-CDR"
    collection_route = "/stocks/collections/stock_zh_a_cdr_daily"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "交易日"},
        {"name": "open", "type": "float64", "description": "-"},
        {"name": "high", "type": "float64", "description": "-"},
        {"name": "low", "type": "float64", "description": "-"},
        {"name": "close", "type": "float64", "description": "-"},
        {"name": "volume", "type": "float64", "description": "注意单位: 手"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
