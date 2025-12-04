"""
港股个股指标服务

亿牛网-港股个股指标: 市盈率, 市净率, 股息率, ROE, 市值
接口: stock_hk_indicator_eniu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_indicator_eniu_provider import StockHkIndicatorEniuProvider


class StockHkIndicatorEniuService(BaseService):
    """港股个股指标服务"""
    
    collection_name = "stock_hk_indicator_eniu"
    provider_class = StockHkIndicatorEniuProvider
    
    # 时间字段名
    time_field = "更新时间"
