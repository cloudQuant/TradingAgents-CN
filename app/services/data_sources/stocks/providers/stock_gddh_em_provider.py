"""
股东大会数据提供者

东方财富网-数据中心-股东大会
接口: stock_gddh_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockGddhEmProvider(SimpleProvider):
    """股东大会数据提供者"""
    
    # 必填属性
    collection_name = "stock_gddh_em"
    display_name = "股东大会"
    akshare_func = "stock_gddh_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股东大会"
    collection_route = "/stocks/collections/stock_gddh_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "召开开始日", "type": "object", "description": "-"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "现场登记日", "type": "object", "description": "-"},
        {"name": "网络投票时间-开始日", "type": "object", "description": "-"},
        {"name": "网络投票时间-结束日", "type": "object", "description": "-"},
        {"name": "决议公告日", "type": "object", "description": "-"},
        {"name": "公告日", "type": "object", "description": "-"},
        {"name": "序列号", "type": "object", "description": "-"},
        {"name": "提案", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
