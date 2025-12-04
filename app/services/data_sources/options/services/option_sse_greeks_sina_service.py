"""期权希腊字母信息表数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseGreeksSinaService(SimpleService):
    """期权希腊字母信息表数据服务"""
    collection_name = "option_sse_greeks_sina"
