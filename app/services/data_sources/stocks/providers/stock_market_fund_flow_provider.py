"""
大盘资金流数据提供者

东方财富网-数据中心-资金流向-大盘
接口: stock_market_fund_flow
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockMarketFundFlowProvider(SimpleProvider):
    """大盘资金流数据提供者"""
    
    # 必填属性
    collection_name = "stock_market_fund_flow"
    display_name = "大盘资金流"
    akshare_func = "stock_market_fund_flow"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-大盘"
    collection_route = "/stocks/collections/stock_market_fund_flow"
    collection_category = "资金流向"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "上证-收盘价", "type": "float64", "description": "-"},
        {"name": "上证-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "深证-收盘价", "type": "float64", "description": "-"},
        {"name": "深证-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "主力净流入-净额", "type": "float64", "description": "-"},
        {"name": "主力净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "超大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "超大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "中单净流入-净额", "type": "float64", "description": "-"},
        {"name": "中单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "小单净流入-净额", "type": "float64", "description": "-"},
        {"name": "小单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
