"""商品期权手续费数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCommInfoService(SimpleService):
    """商品期权手续费数据服务"""
    collection_name = "option_comm_info"
