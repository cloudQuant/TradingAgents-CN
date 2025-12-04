"""
A 股估值指标服务

百度股市通-A 股-财务报表-估值数据
接口: stock_zh_valuation_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_valuation_baidu_provider import StockZhValuationBaiduProvider


class StockZhValuationBaiduService(BaseService):
    """A 股估值指标服务"""
    
    collection_name = "stock_zh_valuation_baidu"
    provider_class = StockZhValuationBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
