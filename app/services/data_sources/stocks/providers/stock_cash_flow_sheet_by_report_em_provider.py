"""
现金流量表-按报告期数据提供者

东方财富-股票-财务分析-现金流量表-按报告期
接口: stock_cash_flow_sheet_by_report_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCashFlowSheetByReportEmProvider(BaseProvider):
    """现金流量表-按报告期数据提供者"""
    
    # 必填属性
    collection_name = "stock_cash_flow_sheet_by_report_em"
    display_name = "现金流量表-按报告期"
    akshare_func = "stock_cash_flow_sheet_by_report_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-股票-财务分析-现金流量表-按报告期"
    collection_route = "/stocks/collections/stock_cash_flow_sheet_by_report_em"
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
        {"name": "-", "type": "-", "description": "252 项，不逐一列出"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
