"""商品期权手续费数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionCommInfoProvider(SimpleProvider):
    """商品期权手续费数据提供者"""
    
    collection_name = "option_comm_info"
    display_name = "商品期权手续费"
    akshare_func = "option_comm_info"
    unique_keys = ["交易所", "品种代码"]
    
    collection_description = "九期网-商品期权手续费数据"
    collection_route = "/options/collections/option_comm_info"
    collection_order = 35
    
    field_info = [
        {"name": "交易所", "type": "string", "description": "交易所"},
        {"name": "品种代码", "type": "string", "description": "品种代码"},
        {"name": "品种名称", "type": "string", "description": "品种名称"},
        {"name": "开仓手续费", "type": "string", "description": "开仓手续费"},
        {"name": "平仓手续费", "type": "string", "description": "平仓手续费"},
        {"name": "平今手续费", "type": "string", "description": "平今手续费"},
        {"name": "行权手续费", "type": "string", "description": "行权手续费"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
