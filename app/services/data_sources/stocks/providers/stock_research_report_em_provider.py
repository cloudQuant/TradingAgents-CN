"""
个股研报数据提供者

东方财富网-数据中心-研究报告-个股研报
接口: stock_research_report_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockResearchReportEmProvider(BaseProvider):
    """个股研报数据提供者"""
    
    # 必填属性
    collection_name = "stock_research_report_em"
    display_name = "个股研报"
    akshare_func = "stock_research_report_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-研究报告-个股研报"
    collection_route = "/stocks/collections/stock_research_report_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "东财评级", "type": "object", "description": "-"},
        {"name": "机构", "type": "object", "description": "-"},
        {"name": "近一月个股研报数", "type": "int64", "description": "-"},
        {"name": "2024-盈利预测-收益", "type": "float64", "description": "-"},
        {"name": "2024-盈利预测-市盈率", "type": "float64", "description": "-"},
        {"name": "2025-盈利预测-收益", "type": "float64", "description": "-"},
        {"name": "2025-盈利预测-市盈率", "type": "float64", "description": "-"},
        {"name": "2026-盈利预测-收益", "type": "float64", "description": "-"},
        {"name": "2026-盈利预测-市盈率", "type": "float64", "description": "-"},
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "报告PDF链接", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
