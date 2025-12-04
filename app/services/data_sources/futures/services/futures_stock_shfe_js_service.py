"""上海期货交易所-库存数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesStockShfeJsService(SimpleService):
    """上海期货交易所-库存数据服务"""
    collection_name = "futures_stock_shfe_js"
