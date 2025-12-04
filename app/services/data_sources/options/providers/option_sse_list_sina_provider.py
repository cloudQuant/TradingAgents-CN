"""上交所50ETF合约到期月份列表数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionSseListSinaProvider(SimpleProvider):
    """上交所50ETF合约到期月份列表数据提供者"""
    
    collection_name = "option_sse_list_sina"
    display_name = "上交所50ETF合约到期月份列表"
    akshare_func = "option_sse_list_sina"
    unique_keys = ["到期月份"]
    
    collection_description = "获取期权上交所50ETF合约到期月份列表"
    collection_route = "/options/collections/option_sse_list_sina"
    collection_order = 17
    
    field_info = [
        {"name": "到期月份", "type": "string", "description": "到期月份"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
