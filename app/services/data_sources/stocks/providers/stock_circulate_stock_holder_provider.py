"""
流通股东数据提供者

新浪财经-股东股本-流通股东
接口: stock_circulate_stock_holder
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCirculateStockHolderProvider(BaseProvider):
    """流通股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_circulate_stock_holder"
    display_name = "流通股东"
    akshare_func = "stock_circulate_stock_holder"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-股东股本-流通股东"
    collection_route = "/stocks/collections/stock_circulate_stock_holder"
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
        {"name": "截止日期", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "编号", "type": "int64", "description": "-"},
        {"name": "持股数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "股本性质", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
