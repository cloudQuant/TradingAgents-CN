"""
龙虎榜-营业部排行-资金实力最强服务

龙虎榜-营业部排行-资金实力最强
接口: stock_lh_yyb_capital
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_lh_yyb_capital_provider import StockLhYybCapitalProvider


class StockLhYybCapitalService(SimpleService):
    """龙虎榜-营业部排行-资金实力最强服务"""
    
    collection_name = "stock_lh_yyb_capital"
    provider_class = StockLhYybCapitalProvider
    
    # 时间字段名
    time_field = "更新时间"
