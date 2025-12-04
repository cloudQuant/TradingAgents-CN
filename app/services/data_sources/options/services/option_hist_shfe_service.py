"""上期所期权数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionHistShfeService(SimpleService):
    """上期所期权数据服务"""
    collection_name = "option_hist_shfe"
