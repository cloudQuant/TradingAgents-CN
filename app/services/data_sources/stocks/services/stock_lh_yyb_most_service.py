"""
龙虎榜-营业部排行-上榜次数最多服务

龙虎榜-营业部排行-上榜次数最多
接口: stock_lh_yyb_most
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_lh_yyb_most_provider import StockLhYybMostProvider


class StockLhYybMostService(SimpleService):
    """龙虎榜-营业部排行-上榜次数最多服务"""
    
    collection_name = "stock_lh_yyb_most"
    provider_class = StockLhYybMostProvider
    
    # 时间字段名
    time_field = "更新时间"
