"""仓单日报-大连商品交易所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesWarehouseReceiptDceService(SimpleService):
    """仓单日报-大连商品交易所数据服务"""
    collection_name = "futures_warehouse_receipt_dce"
