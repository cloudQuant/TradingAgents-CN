"""
两融账户信息服务

东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息
接口: stock_margin_account_info
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_margin_account_info_provider import StockMarginAccountInfoProvider


class StockMarginAccountInfoService(SimpleService):
    """两融账户信息服务"""
    
    collection_name = "stock_margin_account_info"
    provider_class = StockMarginAccountInfoProvider
    
    # 时间字段名
    time_field = "更新时间"
