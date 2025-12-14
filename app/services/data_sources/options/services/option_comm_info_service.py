"""商品期权手续费数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_comm_info_provider import OptionCommInfoProvider


class OptionCommInfoService(SimpleService):
    """商品期权手续费数据服务"""
    collection_name = "option_comm_info"
    provider_class = OptionCommInfoProvider
