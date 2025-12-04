"""
投资评级服务

巨潮资讯-数据中心-评级预测-投资评级
接口: stock_rank_forecast_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_rank_forecast_cninfo_provider import StockRankForecastCninfoProvider


class StockRankForecastCninfoService(BaseService):
    """投资评级服务"""
    
    collection_name = "stock_rank_forecast_cninfo"
    provider_class = StockRankForecastCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
