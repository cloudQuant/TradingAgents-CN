"""港股指数历史行情-新浪数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkIndexDailySinaProvider(BaseProvider):
    """港股指数历史行情-新浪数据提供者"""
    
    collection_name = "stock_hk_index_daily_sina"
    display_name = "港股指数历史行情-新浪"
    akshare_func = "stock_hk_index_daily_sina"
    unique_keys = ["symbol", "date"]
    
    collection_description = "新浪财经-港股指数历史行情数据"
    collection_route = "/indexs/collections/stock_hk_index_daily_sina"
    collection_order = 11
    
    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
    }
    
    # 必填参数
    required_params = ["symbol"]
    
    # 添加参数到数据列
    add_param_columns = {
        "symbol": "symbol",
    }
    
    field_info = [
        {"name": "symbol", "type": "string", "description": "指数代码（如CES100）"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
