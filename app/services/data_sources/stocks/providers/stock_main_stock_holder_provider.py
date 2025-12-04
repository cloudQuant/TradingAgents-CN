"""
主要股东数据提供者

新浪财经-股本股东-主要股东
接口: stock_main_stock_holder
"""
from app.services.data_sources.base_provider import BaseProvider


class StockMainStockHolderProvider(BaseProvider):
    """主要股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_main_stock_holder"
    display_name = "主要股东"
    akshare_func = "stock_main_stock_holder"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-股本股东-主要股东"
    collection_route = "/stocks/collections/stock_main_stock_holder"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "stock": "stock"
    }
    
    # 必填参数
    required_params = ['stock']

    # 字段信息
    field_info = [
        {"name": "编号", "type": "object", "description": "-"},
        {"name": "持股数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "持股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "股本性质", "type": "object", "description": "-"},
        {"name": "截至日期", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "股东说明", "type": "object", "description": "-"},
        {"name": "股东总数", "type": "float64", "description": "-"},
        {"name": "平均持股数", "type": "float64", "description": "备注: 按总股本计算"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
