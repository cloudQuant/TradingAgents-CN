"""商品期权历史行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCommodityHistSinaService(SimpleService):
    """商品期权历史行情数据服务"""
    collection_name = "option_commodity_hist_sina"
