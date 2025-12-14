"""全球指数实时行情-东财数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class IndexGlobalSpotEmProvider(SimpleProvider):
    """全球指数实时行情-东财数据提供者"""
    
    collection_name = "index_global_spot_em"
    display_name = "全球指数实时行情-东财"
    akshare_func = "index_global_spot_em"
    unique_keys = ["代码"]
    
    collection_description = "东方财富网-行情中心-全球指数实时行情数据"
    collection_route = "/indexs/collections/index_global_spot_em"
    collection_order = 30
    
    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "代码", "type": "string", "description": "指数代码"},
        {"name": "名称", "type": "string", "description": "指数名称"},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": ""},
        {"name": "开盘价", "type": "float", "description": ""},
        {"name": "最高价", "type": "float", "description": ""},
        {"name": "最低价", "type": "float", "description": ""},
        {"name": "昨收价", "type": "float", "description": ""},
        {"name": "振幅", "type": "float", "description": ""},
        {"name": "最新行情时间", "type": "string", "description": "注意是指数所在地的时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
