"""广期所隐含波动率数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionVolGfexService(SimpleService):
    """广期所隐含波动率数据服务"""
    collection_name = "option_vol_gfex"
