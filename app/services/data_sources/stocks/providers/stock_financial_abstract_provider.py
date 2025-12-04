"""
关键指标-新浪数据提供者

新浪财经-财务报表-关键指标
接口: stock_financial_abstract
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialAbstractProvider(BaseProvider):
    """关键指标-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_abstract"
    display_name = "关键指标-新浪"
    akshare_func = "stock_financial_abstract"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-财务报表-关键指标"
    collection_route = "/stocks/collections/stock_financial_abstract"
    collection_category = "财务数据"

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
        {"name": "选项", "type": "object", "description": "-"},
        {"name": "指标", "type": "object", "description": "-"},
        {"name": "【具体的报告期】", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
