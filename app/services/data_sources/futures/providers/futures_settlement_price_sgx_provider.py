"""新加坡交易所期货-结算价提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesSettlementPriceSgxProvider(BaseProvider):
    """新加坡交易所期货-结算价提供者"""
    
    collection_name = "futures_settlement_price_sgx"
    display_name = "新加坡交易所期货-结算价"
    akshare_func = "futures_settlement_price_sgx"
    unique_keys = ["日期", "品种"]
    
    collection_description = "新加坡交易所期货结算价"
    collection_route = "/futures/collections/futures_settlement_price_sgx"
    collection_order = 41
    
    param_mapping = {"date": "date"}
    required_params = []
    
    field_info = [
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "结算价", "type": "float", "description": "结算价"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
