"""
股票回购数据服务

东方财富网-数据中心-股票回购-股票回购数据
接口: stock_repurchase_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_repurchase_em_provider import StockRepurchaseEmProvider


class StockRepurchaseEmService(SimpleService):
    """股票回购数据服务"""
    
    collection_name = "stock_repurchase_em"
    provider_class = StockRepurchaseEmProvider
    
    # 时间字段名
    time_field = "更新时间"
