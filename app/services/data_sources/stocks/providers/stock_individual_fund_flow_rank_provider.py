"""
个股资金流排名数据提供者

东方财富网-数据中心-资金流向-排名
接口: stock_individual_fund_flow_rank
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndividualFundFlowRankProvider(BaseProvider):
    """个股资金流排名数据提供者"""
    
    # 必填属性
    collection_name = "stock_individual_fund_flow_rank"
    display_name = "个股资金流排名"
    akshare_func = "stock_individual_fund_flow_rank"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-排名"
    collection_route = "/stocks/collections/stock_individual_fund_flow_rank"
    collection_category = "资金流向"

    # 参数映射
    param_mapping = {
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['indicator']

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "3日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "3日主力净流入-净额", "type": "float64", "description": "-"},
        {"name": "3日主力净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "3日超大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "3日超大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "3日大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "3日大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "3日中单净流入-净额", "type": "float64", "description": "-"},
        {"name": "3日中单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "3日小单净流入-净额", "type": "float64", "description": "-"},
        {"name": "3日小单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "5日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "5日主力净流入-净额", "type": "float64", "description": "-"},
        {"name": "5日主力净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "5日超大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "5日超大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "5日大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "5日大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "5日中单净流入-净额", "type": "float64", "description": "-"},
        {"name": "5日中单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "5日小单净流入-净额", "type": "float64", "description": "-"},
        {"name": "5日小单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "10日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "10日主力净流入-净额", "type": "float64", "description": "-"},
        {"name": "10日主力净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "10日超大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "10日超大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "10日大单净流入-净额", "type": "float64", "description": "-"},
        {"name": "10日大单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "10日中单净流入-净额", "type": "float64", "description": "-"},
        {"name": "10日中单净流入-净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "10日小单净流入-净额", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
