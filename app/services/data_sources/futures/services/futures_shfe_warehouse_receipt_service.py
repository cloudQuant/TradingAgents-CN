"""仓单日报-上海期货交易所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesShfeWarehouseReceiptService(SimpleService):
    """仓单日报-上海期货交易所数据服务"""
    collection_name = "futures_shfe_warehouse_receipt"
