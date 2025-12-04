"""
股票增发数据提供者

新浪财经-发行与分配-增发
接口: stock_add_stock
"""
from app.services.data_sources.base_provider import BaseProvider


class StockAddStockProvider(BaseProvider):
    """股票增发数据提供者"""
    
    # 必填属性
    collection_name = "stock_add_stock"
    display_name = "股票增发"
    akshare_func = "stock_add_stock"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-发行与分配-增发"
    collection_route = "/stocks/collections/stock_add_stock"
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
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "发行方式", "type": "object", "description": "-"},
        {"name": "发行价格", "type": "object", "description": "-"},
        {"name": "实际公司募集资金总额", "type": "object", "description": "-"},
        {"name": "发行费用总额", "type": "object", "description": "-"},
        {"name": "实际发行数量", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
