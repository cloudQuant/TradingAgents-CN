"""
主板市净率服务

乐咕乐股-主板市净率
接口: stock_market_pb_lg
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_market_pb_lg_provider import StockMarketPbLgProvider


class StockMarketPbLgService(BaseService):
    """主板市净率服务"""
    
    collection_name = "stock_market_pb_lg"
    provider_class = StockMarketPbLgProvider
    
    # 时间字段名
    time_field = "更新时间"
