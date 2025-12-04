"""
大盘拥挤度服务

乐咕乐股-大盘拥挤度
接口: stock_a_congestion_lg
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_a_congestion_lg_provider import StockACongestionLgProvider


class StockACongestionLgService(SimpleService):
    """大盘拥挤度服务"""
    
    collection_name = "stock_a_congestion_lg"
    provider_class = StockACongestionLgProvider
    
    # 时间字段名
    time_field = "更新时间"
