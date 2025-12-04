"""
大单追踪数据提供者

同花顺-数据中心-资金流向-大单追踪
接口: stock_fund_flow_big_deal
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockFundFlowBigDealProvider(SimpleProvider):
    """大单追踪数据提供者"""
    
    # 必填属性
    collection_name = "stock_fund_flow_big_deal"
    display_name = "大单追踪"
    akshare_func = "stock_fund_flow_big_deal"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-资金流向-大单追踪"
    collection_route = "/stocks/collections/stock_fund_flow_big_deal"
    collection_category = "资金流向"

    # 字段信息
    field_info = [
        {"name": "成交时间", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "int64", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "成交价格", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "int64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "大单性质", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "object", "description": "-"},
        {"name": "涨跌额", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
