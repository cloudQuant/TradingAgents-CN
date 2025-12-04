"""
个股限售解禁-新浪数据提供者

新浪财经-发行分配-限售解禁
接口: stock_restricted_release_queue_sina
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRestrictedReleaseQueueSinaProvider(BaseProvider):
    """个股限售解禁-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_restricted_release_queue_sina"
    display_name = "个股限售解禁-新浪"
    akshare_func = "stock_restricted_release_queue_sina"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-发行分配-限售解禁"
    collection_route = "/stocks/collections/stock_restricted_release_queue_sina"
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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "解禁日期", "type": "object", "description": "-"},
        {"name": "解禁数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "解禁股流通市值", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "上市批次", "type": "int64", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
