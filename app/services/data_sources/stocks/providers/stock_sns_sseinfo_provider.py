"""
上证e互动数据提供者

上证e互动-提问与回答
接口: stock_sns_sseinfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSnsSseinfoProvider(BaseProvider):
    """上证e互动数据提供者"""
    
    # 必填属性
    collection_name = "stock_sns_sseinfo"
    display_name = "上证e互动"
    akshare_func = "stock_sns_sseinfo"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "上证e互动-提问与回答"
    collection_route = "/stocks/collections/stock_sns_sseinfo"
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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "公司简称", "type": "object", "description": "-"},
        {"name": "问题", "type": "object", "description": "-"},
        {"name": "回答", "type": "object", "description": "-"},
        {"name": "问题时间", "type": "object", "description": "-"},
        {"name": "回答时间", "type": "object", "description": "-"},
        {"name": "问题来源", "type": "object", "description": "-"},
        {"name": "回答来源", "type": "object", "description": "-"},
        {"name": "用户名", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
