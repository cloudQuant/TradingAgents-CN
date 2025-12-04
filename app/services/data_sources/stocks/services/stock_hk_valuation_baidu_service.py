"""
港股估值指标服务

百度股市通-港股-财务报表-估值数据
接口: stock_hk_valuation_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_valuation_baidu_provider import StockHkValuationBaiduProvider


class StockHkValuationBaiduService(BaseService):
    """港股估值指标服务"""
    
    collection_name = "stock_hk_valuation_baidu"
    provider_class = StockHkValuationBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
