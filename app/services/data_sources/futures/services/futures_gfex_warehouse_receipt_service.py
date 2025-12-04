"""仓单日报-广州期货交易所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesGfexWarehouseReceiptService(SimpleService):
    """仓单日报-广州期货交易所数据服务"""
    collection_name = "futures_gfex_warehouse_receipt"
