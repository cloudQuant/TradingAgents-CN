"""
库存数据-东方财富数据服务

支持批量更新：从 futures_fees_info 集合获取品种代码进行批量更新
"""
from app.services.data_sources.futures.services.symbol_batch_service import SymbolBatchService
from app.services.data_sources.futures.providers.futures_inventory_em_provider import FuturesInventoryEmProvider


class FuturesInventoryEmService(SymbolBatchService):
    """库存数据-东方财富数据服务"""
    
    collection_name = "futures_inventory_em"
    provider_class = FuturesInventoryEmProvider
    
    # symbol来源配置
    SYMBOL_SOURCE_COLLECTION = "futures_fees_info"
    SYMBOL_SOURCE_FIELD = "品种代码"
    
    time_field = "日期"
    unique_keys = ["品种代码", "日期"]
