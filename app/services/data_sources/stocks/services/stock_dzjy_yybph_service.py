"""
营业部排行服务

东方财富网-数据中心-大宗交易-营业部排行
接口: stock_dzjy_yybph
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_dzjy_yybph_provider import StockDzjyYybphProvider


class StockDzjyYybphService(BaseService):
    """营业部排行服务"""
    
    collection_name = "stock_dzjy_yybph"
    provider_class = StockDzjyYybphProvider
    
    # 时间字段名
    time_field = "更新时间"
