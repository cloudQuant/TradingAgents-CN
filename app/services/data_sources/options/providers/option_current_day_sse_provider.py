"""上交所当日合约数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionCurrentDaySseProvider(SimpleProvider):
    """上交所当日合约数据提供者"""
    
    collection_name = "option_current_day_sse"
    display_name = "上交所当日合约"
    akshare_func = "option_current_day_sse"
    unique_keys = ["合约编码"]
    
    collection_description = "上海证券交易所-产品-股票期权-信息披露-当日合约"
    collection_route = "/options/collections/option_current_day_sse"
    collection_order = 4
    
    field_info = [
        {"name": "合约编码", "type": "string", "description": "合约编码"},
        {"name": "合约交易代码", "type": "string", "description": "合约交易代码"},
        {"name": "合约简称", "type": "string", "description": "合约简称"},
        {"name": "标的券名称及代码", "type": "string", "description": "标的券名称及代码"},
        {"name": "类型", "type": "string", "description": "类型"},
        {"name": "行权价", "type": "string", "description": "行权价"},
        {"name": "合约单位", "type": "string", "description": "合约单位"},
        {"name": "期权行权日", "type": "string", "description": "期权行权日"},
        {"name": "行权交收日", "type": "string", "description": "行权交收日"},
        {"name": "到期日", "type": "string", "description": "到期日"},
        {"name": "开始日期", "type": "string", "description": "开始日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
