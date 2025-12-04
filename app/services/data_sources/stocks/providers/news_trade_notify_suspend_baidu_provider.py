"""
停复牌数据提供者

百度股市通-交易提醒-停复牌
接口: news_trade_notify_suspend_baidu
"""
from app.services.data_sources.base_provider import BaseProvider


class NewsTradeNotifySuspendBaiduProvider(BaseProvider):
    """停复牌数据提供者"""
    
    # 必填属性
    collection_name = "news_trade_notify_suspend_baidu"
    display_name = "停复牌"
    akshare_func = "news_trade_notify_suspend_baidu"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "百度股市通-交易提醒-停复牌"
    collection_route = "/stocks/collections/news_trade_notify_suspend_baidu"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "交易所", "type": "object", "description": "-"},
        {"name": "停牌时间", "type": "object", "description": "-"},
        {"name": "复牌时间", "type": "object", "description": "-"},
        {"name": "停牌事项说明", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
