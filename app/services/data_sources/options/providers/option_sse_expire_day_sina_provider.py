"""剩余到期时间数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionSseExpireDaySinaProvider(BaseProvider):
    """剩余到期时间数据提供者"""
    
    collection_name = "option_sse_expire_day_sina"
    display_name = "剩余到期时间"
    akshare_func = "option_sse_expire_day_sina"
    unique_keys = ["到期月份", "品种"]
    
    collection_description = "获取指定到期月份指定品种的剩余到期时间"
    collection_route = "/options/collections/option_sse_expire_day_sina"
    collection_order = 18
    
    param_mapping = {"trade_date": "trade_date", "symbol": "symbol"}
    required_params = ["trade_date", "symbol"]
    add_param_columns = {"trade_date": "到期月份", "symbol": "品种"}
    
    field_info = [
        {"name": "到期月份", "type": "string", "description": "到期月份"},
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "剩余天数", "type": "int", "description": "剩余到期天数"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
