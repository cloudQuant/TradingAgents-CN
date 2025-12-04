"""
沪深京 A 股公告数据提供者

东方财富网-数据中心-公告大全-沪深京 A 股公告
接口: stock_notice_report
"""
from app.services.data_sources.base_provider import BaseProvider


class StockNoticeReportProvider(BaseProvider):
    """沪深京 A 股公告数据提供者"""
    
    # 必填属性
    collection_name = "stock_notice_report"
    display_name = "沪深京 A 股公告"
    akshare_func = "stock_notice_report"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-公告大全-沪深京 A 股公告"
    collection_route = "/stocks/collections/stock_notice_report"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "公告标题", "type": "object", "description": "-"},
        {"name": "公告类型", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "网址", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
