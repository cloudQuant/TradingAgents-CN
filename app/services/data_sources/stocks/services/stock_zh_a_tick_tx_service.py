"""
腾讯财经服务

每个交易日 16:00 提供当日数据; 如遇到数据缺失, 请使用 **ak.stock_zh_a_tick_163()** 接口(注意数据会有一定差异)
接口: stock_zh_a_tick_tx
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_tick_tx_provider import StockZhATickTxProvider


class StockZhATickTxService(BaseService):
    """腾讯财经服务"""
    
    collection_name = "stock_zh_a_tick_tx"
    provider_class = StockZhATickTxProvider
    
    # 时间字段名
    time_field = "更新时间"
