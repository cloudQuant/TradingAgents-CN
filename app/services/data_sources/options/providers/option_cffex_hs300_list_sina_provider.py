"""中金所沪深300指数合约列表数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionCffexHs300ListSinaProvider(SimpleProvider):
    """中金所沪深300指数合约列表数据提供者"""
    
    collection_name = "option_cffex_hs300_list_sina"
    display_name = "中金所沪深300指数合约列表"
    akshare_func = "option_cffex_hs300_list_sina"
    unique_keys = ["合约代码"]
    
    collection_description = "中金所沪深300指数所有合约，返回的第一个合约为主力合约"
    collection_route = "/options/collections/option_cffex_hs300_list_sina"
    collection_order = 9
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
