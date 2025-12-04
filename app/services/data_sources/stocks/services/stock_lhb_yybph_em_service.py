"""
营业部排行服务

东方财富网-数据中心-龙虎榜单-营业部排行
接口: stock_lhb_yybph_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_yybph_em_provider import StockLhbYybphEmProvider


class StockLhbYybphEmService(BaseService):
    """营业部排行服务"""
    
    collection_name = "stock_lhb_yybph_em"
    provider_class = StockLhbYybphEmProvider
    
    # 时间字段名
    time_field = "更新时间"
