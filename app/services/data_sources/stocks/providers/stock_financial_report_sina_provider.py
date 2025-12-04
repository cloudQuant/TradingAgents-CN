"""
财务报表-新浪数据提供者

新浪财经-财务报表-三大报表
接口: stock_financial_report_sina
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialReportSinaProvider(BaseProvider):
    """财务报表-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_report_sina"
    display_name = "财务报表-新浪"
    akshare_func = "stock_financial_report_sina"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-财务报表-三大报表"
    collection_route = "/stocks/collections/stock_financial_report_sina"
    collection_category = "财务数据"

    # 参数映射
    param_mapping = {
        "stock": "stock",
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['stock', 'symbol']

    # 字段信息
    field_info = [
        {"name": "报告日", "type": "object", "description": "报告日期"},
        {"name": "流动资产", "type": "object", "description": "-"},
        {"name": "...", "type": "object", "description": "-"},
        {"name": "类型", "type": "object", "description": "-"},
        {"name": "更新日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
