"""
恒生指数股息率数据提供者

乐咕乐股-股息率-恒生指数股息率
接口: stock_hk_gxl_lg
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkGxlLgProvider(SimpleProvider):
    """恒生指数股息率数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_gxl_lg"
    display_name = "恒生指数股息率"
    akshare_func = "stock_hk_gxl_lg"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-股息率-恒生指数股息率"
    collection_route = "/stocks/collections/stock_hk_gxl_lg"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "股息率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
