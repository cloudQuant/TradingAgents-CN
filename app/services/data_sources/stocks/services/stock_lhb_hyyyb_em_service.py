"""
每日活跃营业部服务

东方财富网-数据中心-龙虎榜单-每日活跃营业部
接口: stock_lhb_hyyyb_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_hyyyb_em_provider import StockLhbHyyybEmProvider


class StockLhbHyyybEmService(BaseService):
    """每日活跃营业部服务"""
    
    collection_name = "stock_lhb_hyyyb_em"
    provider_class = StockLhbHyyybEmProvider
    
    # 时间字段名
    time_field = "更新时间"
