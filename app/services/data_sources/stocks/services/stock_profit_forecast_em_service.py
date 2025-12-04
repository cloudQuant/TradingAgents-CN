"""
盈利预测-东方财富服务

东方财富网-数据中心-研究报告-盈利预测; 该数据源网页端返回数据有异常, 本接口已修复该异常
接口: stock_profit_forecast_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profit_forecast_em_provider import StockProfitForecastEmProvider


class StockProfitForecastEmService(BaseService):
    """盈利预测-东方财富服务"""
    
    collection_name = "stock_profit_forecast_em"
    provider_class = StockProfitForecastEmProvider
    
    # 时间字段名
    time_field = "更新时间"
