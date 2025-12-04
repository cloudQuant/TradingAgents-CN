"""
盈利预测-同花顺服务

同花顺-盈利预测
接口: stock_profit_forecast_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profit_forecast_ths_provider import StockProfitForecastThsProvider


class StockProfitForecastThsService(BaseService):
    """盈利预测-同花顺服务"""
    
    collection_name = "stock_profit_forecast_ths"
    provider_class = StockProfitForecastThsProvider
    
    # 时间字段名
    time_field = "更新时间"
