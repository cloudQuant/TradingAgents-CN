"""
活跃 A 股统计服务

东方财富网-数据中心-大宗交易-活跃 A 股统计
接口: stock_dzjy_hygtj
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_dzjy_hygtj_provider import StockDzjyHygtjProvider


class StockDzjyHygtjService(BaseService):
    """活跃 A 股统计服务"""
    
    collection_name = "stock_dzjy_hygtj"
    provider_class = StockDzjyHygtjProvider
    
    # 时间字段名
    time_field = "更新时间"
