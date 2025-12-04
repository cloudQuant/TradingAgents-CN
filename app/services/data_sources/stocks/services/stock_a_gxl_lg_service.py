"""
A 股股息率服务

乐咕乐股-股息率-A 股股息率
接口: stock_a_gxl_lg
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_a_gxl_lg_provider import StockAGxlLgProvider


class StockAGxlLgService(BaseService):
    """A 股股息率服务"""
    
    collection_name = "stock_a_gxl_lg"
    provider_class = StockAGxlLgProvider
    
    # 时间字段名
    time_field = "更新时间"
