"""
分红派息数据提供者

百度股市通-交易提醒-分红派息
接口: news_trade_notify_dividend_baidu
"""
from app.services.data_sources.base_provider import BaseProvider


class NewsTradeNotifyDividendBaiduProvider(BaseProvider):
    """分红派息数据提供者"""
    
    # 必填属性
    collection_name = "news_trade_notify_dividend_baidu"
    display_name = "分红派息"
    akshare_func = "news_trade_notify_dividend_baidu"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "百度股市通-交易提醒-分红派息"
    collection_route = "/stocks/collections/news_trade_notify_dividend_baidu"
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
        {"name": "除权日", "type": "object", "description": "-"},
        {"name": "分红", "type": "object", "description": "-"},
        {"name": "送股", "type": "object", "description": "-"},
        {"name": "转增", "type": "object", "description": "-"},
        {"name": "实物", "type": "object", "description": "-"},
        {"name": "交易所", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "报告期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
