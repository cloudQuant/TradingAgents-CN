"""生猪市场价格指数提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class IndexHogSpotPriceProvider(SimpleProvider):
    """生猪市场价格指数提供者"""
    
    collection_name = "index_hog_spot_price"
    display_name = "生猪市场价格指数"
    akshare_func = "index_hog_spot_price"
    unique_keys = ["日期"]
    
    collection_description = "生猪市场价格指数"
    collection_route = "/futures/collections/index_hog_spot_price"
    collection_order = 51
    
    field_info = [
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "指数", "type": "float", "description": "价格指数"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
