"""
基金持股数据提供者

新浪财经-股本股东-基金持股
接口: stock_fund_stock_holder
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFundStockHolderProvider(BaseProvider):
    """基金持股数据提供者"""
    
    # 必填属性
    collection_name = "stock_fund_stock_holder"
    display_name = "基金持股"
    akshare_func = "stock_fund_stock_holder"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-股本股东-基金持股"
    collection_route = "/stocks/collections/stock_fund_stock_holder"
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
        {"name": "基金代码", "type": "object", "description": "-"},
        {"name": "持仓数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "持股市值", "type": "int64", "description": "注意单位: 元"},
        {"name": "占净值比例", "type": "float64", "description": "注意单位: %"},
        {"name": "截止日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
