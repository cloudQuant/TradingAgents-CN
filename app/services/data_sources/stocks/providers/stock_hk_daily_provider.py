"""
历史行情数据-新浪数据提供者

港股-历史行情数据, 可以选择返回复权后数据,更新频率为日频
接口: stock_hk_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkDailyProvider(BaseProvider):
    """历史行情数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_daily"
    display_name = "历史行情数据-新浪"
    akshare_func = "stock_hk_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "港股-历史行情数据, 可以选择返回复权后数据,更新频率为日频"
    collection_route = "/stocks/collections/stock_hk_daily"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "volume", "type": "float64", "description": "成交量"},
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "volume", "type": "float64", "description": "成交量"},
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "hfq_factor", "type": "object", "description": "后复权因子"},
        {"name": "cash", "type": "object", "description": "现金分红"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
