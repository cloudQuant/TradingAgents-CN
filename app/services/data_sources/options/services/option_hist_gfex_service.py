"""广期所期权数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionHistGfexService(SimpleService):
    """广期所期权数据服务"""
    collection_name = "option_hist_gfex"
