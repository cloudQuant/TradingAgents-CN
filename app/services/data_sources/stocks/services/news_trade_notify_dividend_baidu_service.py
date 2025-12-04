"""
分红派息服务

百度股市通-交易提醒-分红派息
接口: news_trade_notify_dividend_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.news_trade_notify_dividend_baidu_provider import NewsTradeNotifyDividendBaiduProvider


class NewsTradeNotifyDividendBaiduService(BaseService):
    """分红派息服务"""
    
    collection_name = "news_trade_notify_dividend_baidu"
    provider_class = NewsTradeNotifyDividendBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
