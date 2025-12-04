"""
内部交易服务

雪球-行情中心-沪深股市-内部交易
接口: stock_inner_trade_xq
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_inner_trade_xq_provider import StockInnerTradeXqProvider


class StockInnerTradeXqService(SimpleService):
    """内部交易服务"""
    
    collection_name = "stock_inner_trade_xq"
    provider_class = StockInnerTradeXqProvider
    
    # 时间字段名
    time_field = "更新时间"
