"""期权龙虎榜数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_lhb_em_provider import OptionLhbEmProvider


class OptionLhbEmService(SimpleService):
    """期权龙虎榜数据服务"""
    collection_name = "option_lhb_em"
    provider_class = OptionLhbEmProvider
