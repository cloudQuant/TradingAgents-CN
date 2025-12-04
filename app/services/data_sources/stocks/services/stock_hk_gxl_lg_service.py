"""
恒生指数股息率服务

乐咕乐股-股息率-恒生指数股息率
接口: stock_hk_gxl_lg
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hk_gxl_lg_provider import StockHkGxlLgProvider


class StockHkGxlLgService(SimpleService):
    """恒生指数股息率服务"""
    
    collection_name = "stock_hk_gxl_lg"
    provider_class = StockHkGxlLgProvider
    
    # 时间字段名
    time_field = "更新时间"
