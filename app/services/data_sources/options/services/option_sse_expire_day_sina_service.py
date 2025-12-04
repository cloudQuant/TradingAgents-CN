"""剩余到期时间数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionSseExpireDaySinaService(SimpleService):
    """剩余到期时间数据服务"""
    collection_name = "option_sse_expire_day_sina"
