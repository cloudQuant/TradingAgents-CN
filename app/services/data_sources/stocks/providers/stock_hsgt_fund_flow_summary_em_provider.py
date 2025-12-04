"""
沪深港通资金流向数据提供者

东方财富网-数据中心-资金流向-沪深港通资金流向
接口: stock_hsgt_fund_flow_summary_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHsgtFundFlowSummaryEmProvider(SimpleProvider):
    """沪深港通资金流向数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_fund_flow_summary_em"
    display_name = "沪深港通资金流向"
    akshare_func = "stock_hsgt_fund_flow_summary_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-沪深港通资金流向"
    collection_route = "/stocks/collections/stock_hsgt_fund_flow_summary_em"
    collection_category = "资金流向"

    # 字段信息
    field_info = [
        {"name": "交易日", "type": "object", "description": "-"},
        {"name": "类型", "type": "object", "description": "-"},
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "资金方向", "type": "object", "description": "-"},
        {"name": "交易状态", "type": "int64", "description": "3 为收盘"},
        {"name": "成交净买额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "资金净流入", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "当日资金余额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "上涨数", "type": "int64", "description": "-"},
        {"name": "持平数", "type": "int64", "description": "-"},
        {"name": "下跌数", "type": "int64", "description": "-"},
        {"name": "相关指数", "type": "object", "description": "-"},
        {"name": "指数涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
