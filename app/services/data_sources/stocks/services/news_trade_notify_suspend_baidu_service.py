"""
停复牌服务

百度股市通-交易提醒-停复牌
接口: news_trade_notify_suspend_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.news_trade_notify_suspend_baidu_provider import NewsTradeNotifySuspendBaiduProvider


class NewsTradeNotifySuspendBaiduService(BaseService):
    """停复牌服务"""
    
    collection_name = "news_trade_notify_suspend_baidu"
    provider_class = NewsTradeNotifySuspendBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
