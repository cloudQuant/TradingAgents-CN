"""仓单日报-郑州商品交易所数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesWarehouseReceiptCzceProvider(BaseProvider):
    """仓单日报-郑州商品交易所数据提供者"""
    
    collection_name = "futures_warehouse_receipt_czce"
    display_name = "仓单日报-郑州商品交易所"
    akshare_func = "futures_czce_warehouse_receipt"
    unique_keys = ["日期", "品种", "仓库"]
    
    collection_description = "郑州商品交易所仓单日报数据"
    collection_route = "/futures/collections/futures_warehouse_receipt_czce"
    collection_order = 8
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "仓库", "type": "string", "description": "仓库名称"},
        {"name": "仓单数量", "type": "float", "description": "仓单数量"},
        {"name": "增减", "type": "float", "description": "增减量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
