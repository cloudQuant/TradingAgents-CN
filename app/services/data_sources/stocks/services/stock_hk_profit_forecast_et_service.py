"""
港股盈利预测-经济通服务

经济通-公司资料-盈利预测
接口: stock_hk_profit_forecast_et
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_profit_forecast_et_provider import StockHkProfitForecastEtProvider


class StockHkProfitForecastEtService(BaseService):
    """港股盈利预测-经济通服务"""
    
    collection_name = "stock_hk_profit_forecast_et"
    provider_class = StockHkProfitForecastEtProvider
    
    # 时间字段名
    time_field = "更新时间"
