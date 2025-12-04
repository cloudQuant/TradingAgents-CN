"""
行业个股资金流数据提供者

东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流
接口: stock_sector_fund_flow_summary
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSectorFundFlowSummaryProvider(BaseProvider):
    """行业个股资金流数据提供者"""
    
    # 必填属性
    collection_name = "stock_sector_fund_flow_summary"
    display_name = "行业个股资金流"
    akshare_func = "stock_sector_fund_flow_summary"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流"
    collection_route = "/stocks/collections/stock_sector_fund_flow_summary"
    collection_category = "资金流向"

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "今日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "今日主力净流入-净额", "type": "float64", "description": "-"},
        {"name": "今日主力净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日超大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "今日超大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "今日大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日中单净流入-净额", "type": "float64", "description": "-"},
        {"name": "今日中单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日小单净流入-净额", "type": "float64", "description": "-"},
        {"name": "今日小单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
