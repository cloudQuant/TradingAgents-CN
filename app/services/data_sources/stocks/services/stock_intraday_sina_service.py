"""
日内分时数据-新浪服务

新浪财经-日内分时数据
接口: stock_intraday_sina
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_intraday_sina_provider import StockIntradaySinaProvider


class StockIntradaySinaService(BaseService):
    """日内分时数据-新浪服务"""
    
    collection_name = "stock_intraday_sina"
    provider_class = StockIntradaySinaProvider
    
    # 时间字段名
    time_field = "更新时间"
