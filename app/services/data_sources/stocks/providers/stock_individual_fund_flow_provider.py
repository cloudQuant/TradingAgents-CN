"""
个股资金流数据提供者

东方财富网-数据中心-个股资金流向
接口: stock_individual_fund_flow
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndividualFundFlowProvider(BaseProvider):
    """个股资金流数据提供者"""
    
    # 必填属性
    collection_name = "stock_individual_fund_flow"
    display_name = "个股资金流"
    akshare_func = "stock_individual_fund_flow"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-个股资金流向"
    collection_route = "/stocks/collections/stock_individual_fund_flow"
    collection_category = "资金流向"

    # 参数映射
    param_mapping = {
        "stock": "stock",
        "market": "market"
    }
    
    # 必填参数
    required_params = ['stock', 'market']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
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
