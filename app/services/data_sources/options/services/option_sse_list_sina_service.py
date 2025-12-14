"""上交所50ETF合约到期月份列表数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_sse_list_sina_provider import OptionSseListSinaProvider


class OptionSseListSinaService(SimpleService):
    """上交所50ETF合约到期月份列表数据服务"""
    collection_name = "option_sse_list_sina"
    provider_class = OptionSseListSinaProvider
