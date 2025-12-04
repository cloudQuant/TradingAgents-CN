"""
财报发行数据提供者

百度股市通-财报发行
接口: news_report_time_baidu
"""
from app.services.data_sources.base_provider import BaseProvider


class NewsReportTimeBaiduProvider(BaseProvider):
    """财报发行数据提供者"""
    
    # 必填属性
    collection_name = "news_report_time_baidu"
    display_name = "财报发行"
    akshare_func = "news_report_time_baidu"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "百度股市通-财报发行"
    collection_route = "/stocks/collections/news_report_time_baidu"
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
        {"name": "交易所", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "财报期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
