"""
仓单日报-大连商品交易所数据服务

支持增量更新：从数据库最大日期开始更新到今天
"""
from app.services.data_sources.futures.services.date_incremental_service import DateIncrementalService
from app.services.data_sources.futures.providers.futures_warehouse_receipt_dce_provider import FuturesWarehouseReceiptDceProvider


class FuturesWarehouseReceiptDceService(DateIncrementalService):
    """仓单日报-大连商品交易所数据服务"""
    
    collection_name = "futures_warehouse_receipt_dce"
    provider_class = FuturesWarehouseReceiptDceProvider
    
    time_field = "日期"
    unique_keys = ["日期", "品种"]
    DEFAULT_START_DATE = "20100101"
