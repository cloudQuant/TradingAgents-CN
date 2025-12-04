"""看涨看跌合约代码数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseCodesSinaService(SimpleService):
    """看涨看跌合约代码数据服务"""
    collection_name = "option_sse_codes_sina"
