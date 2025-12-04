"""
市场统计服务

东方财富网-数据中心-大宗交易-市场统计
接口: stock_dzjy_sctj
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_dzjy_sctj_provider import StockDzjySctjProvider


class StockDzjySctjService(SimpleService):
    """市场统计服务"""
    
    collection_name = "stock_dzjy_sctj"
    provider_class = StockDzjySctjProvider
    
    # 时间字段名
    time_field = "更新时间"
