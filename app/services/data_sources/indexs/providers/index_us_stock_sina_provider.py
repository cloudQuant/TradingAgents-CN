"""美股指数行情-新浪数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class IndexUsStockSinaProvider(BaseProvider):
    """美股指数行情-新浪数据提供者"""
    
    collection_name = "index_us_stock_sina"
    display_name = "美股指数行情-新浪"
    akshare_func = "index_us_stock_sina"
    unique_keys = ["symbol", "date"]
    
    collection_description = "新浪财经-美股指数行情数据（纳斯达克、道琼斯、标普500等）"
    collection_route = "/indexs/collections/index_us_stock_sina"
    collection_order = 20
    
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
        {"name": "symbol", "type": "string", "description": "指数代码（.IXIC/.DJI/.INX/.NDX）"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "int", "description": "成交量"},
        {"name": "amount", "type": "int", "description": "成交额"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
