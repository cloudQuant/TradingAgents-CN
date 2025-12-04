"""
信息披露调研-巨潮资讯数据提供者

巨潮资讯-首页-公告查询-信息披露调研-沪深京
接口: stock_zh_a_disclosure_relation_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhADisclosureRelationCninfoProvider(BaseProvider):
    """信息披露调研-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_disclosure_relation_cninfo"
    display_name = "信息披露调研-巨潮资讯"
    akshare_func = "stock_zh_a_disclosure_relation_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-首页-公告查询-信息披露调研-沪深京"
    collection_route = "/stocks/collections/stock_zh_a_disclosure_relation_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "market": "market",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol', 'market', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "公告标题", "type": "object", "description": "-"},
        {"name": "公告时间", "type": "object", "description": "-"},
        {"name": "公告链接", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
