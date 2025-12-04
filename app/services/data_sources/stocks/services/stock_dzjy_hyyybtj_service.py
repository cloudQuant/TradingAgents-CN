"""
活跃营业部统计服务

东方财富网-数据中心-大宗交易-活跃营业部统计
接口: stock_dzjy_hyyybtj
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_dzjy_hyyybtj_provider import StockDzjyHyyybtjProvider


class StockDzjyHyyybtjService(BaseService):
    """活跃营业部统计服务"""
    
    collection_name = "stock_dzjy_hyyybtj"
    provider_class = StockDzjyHyyybtjProvider
    
    # 时间字段名
    time_field = "更新时间"
