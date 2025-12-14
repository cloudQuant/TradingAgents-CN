"""广期所隐含波动率数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_vol_gfex_provider import OptionVolGfexProvider


class OptionVolGfexService(SimpleService):
    """广期所隐含波动率数据服务"""
    collection_name = "option_vol_gfex"
    provider_class = OptionVolGfexProvider
