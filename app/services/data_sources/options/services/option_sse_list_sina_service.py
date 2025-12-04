"""上交所50ETF合约到期月份列表数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseListSinaService(SimpleService):
    """上交所50ETF合约到期月份列表数据服务"""
    collection_name = "option_sse_list_sina"
