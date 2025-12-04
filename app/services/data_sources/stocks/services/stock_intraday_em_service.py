"""
日内分时数据-东财服务

东方财富-分时数据
接口: stock_intraday_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_intraday_em_provider import StockIntradayEmProvider


class StockIntradayEmService(BaseService):
    """日内分时数据-东财服务"""
    
    collection_name = "stock_intraday_em"
    provider_class = StockIntradayEmProvider
    
    # 时间字段名
    time_field = "更新时间"
