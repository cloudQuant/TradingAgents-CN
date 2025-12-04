"""
证券类别统计数据提供者

深圳证券交易所-市场总貌-证券类别统计
接口: stock_szse_summary
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSzseSummaryProvider(BaseProvider):
    """证券类别统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_szse_summary"
    display_name = "证券类别统计"
    akshare_func = "stock_szse_summary"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深圳证券交易所-市场总貌-证券类别统计"
    collection_route = "/stocks/collections/stock_szse_summary"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "证券类别", "type": "object", "description": "-"},
        {"name": "数量", "type": "int64", "description": "注意单位: 只"},
        {"name": "成交金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "总市值", "type": "float64", "description": "-"},
        {"name": "流通市值", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
