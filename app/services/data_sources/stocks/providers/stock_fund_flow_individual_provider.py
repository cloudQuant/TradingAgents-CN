"""
个股资金流数据提供者

同花顺-数据中心-资金流向-个股资金流
接口: stock_fund_flow_individual
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFundFlowIndividualProvider(BaseProvider):
    """个股资金流数据提供者"""
    
    # 必填属性
    collection_name = "stock_fund_flow_individual"
    display_name = "个股资金流"
    akshare_func = "stock_fund_flow_individual"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-资金流向-个股资金流"
    collection_route = "/stocks/collections/stock_fund_flow_individual"
    collection_category = "资金流向"

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
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "股票代码", "type": "int64", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "换手率", "type": "object", "description": "-"},
        {"name": "流入资金", "type": "object", "description": "注意单位: 元"},
        {"name": "流出资金", "type": "object", "description": "注意单位: 元"},
        {"name": "净额", "type": "object", "description": "注意单位: 元"},
        {"name": "成交额", "type": "object", "description": "注意单位: 元"},
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "股票代码", "type": "int64", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "阶段涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "连续换手率", "type": "object", "description": "注意单位: %"},
        {"name": "资金流入净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
