"""仓单日报-郑州商品交易所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesWarehouseReceiptCzceService(SimpleService):
    """仓单日报-郑州商品交易所数据服务"""
    collection_name = "futures_warehouse_receipt_czce"
