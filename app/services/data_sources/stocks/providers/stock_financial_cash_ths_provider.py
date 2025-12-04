"""
现金流量表数据提供者

同花顺-财务指标-现金流量表
接口: stock_financial_cash_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialCashThsProvider(BaseProvider):
    """现金流量表数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_cash_ths"
    display_name = "现金流量表"
    akshare_func = "stock_financial_cash_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-财务指标-现金流量表"
    collection_route = "/stocks/collections/stock_financial_cash_ths"
    collection_category = "财务数据"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "-", "type": "-", "description": "75 项，不逐一列出"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
