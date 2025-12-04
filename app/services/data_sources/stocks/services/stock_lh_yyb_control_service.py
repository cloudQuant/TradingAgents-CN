"""
龙虎榜-营业部排行-抱团操作实力服务

龙虎榜-营业部排行-抱团操作实力
接口: stock_lh_yyb_control
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_lh_yyb_control_provider import StockLhYybControlProvider


class StockLhYybControlService(SimpleService):
    """龙虎榜-营业部排行-抱团操作实力服务"""
    
    collection_name = "stock_lh_yyb_control"
    provider_class = StockLhYybControlProvider
    
    # 时间字段名
    time_field = "更新时间"
