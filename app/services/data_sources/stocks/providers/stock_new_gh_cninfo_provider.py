"""
新股过会数据提供者

巨潮资讯-数据中心-新股数据-新股过会
接口: stock_new_gh_cninfo
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockNewGhCninfoProvider(SimpleProvider):
    """新股过会数据提供者"""
    
    # 必填属性
    collection_name = "stock_new_gh_cninfo"
    display_name = "新股过会"
    akshare_func = "stock_new_gh_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-新股数据-新股过会"
    collection_route = "/stocks/collections/stock_new_gh_cninfo"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "上会日期", "type": "object", "description": "-"},
        {"name": "审核类型", "type": "object", "description": "-"},
        {"name": "审议内容", "type": "object", "description": "-"},
        {"name": "审核结果", "type": "object", "description": "-"},
        {"name": "审核公告日", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
