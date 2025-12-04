"""
美港目标价服务

美港电讯-美港目标价数据
接口: stock_price_js
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_price_js_provider import StockPriceJsProvider


class StockPriceJsService(BaseService):
    """美港目标价服务"""
    
    collection_name = "stock_price_js"
    provider_class = StockPriceJsProvider
    
    # 时间字段名
    time_field = "更新时间"
