"""
行业资金流数据提供者

同花顺-数据中心-资金流向-行业资金流
接口: stock_fund_flow_industry
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFundFlowIndustryProvider(BaseProvider):
    """行业资金流数据提供者"""
    
    # 必填属性
    collection_name = "stock_fund_flow_industry"
    display_name = "行业资金流"
    akshare_func = "stock_fund_flow_industry"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-资金流向-行业资金流"
    collection_route = "/stocks/collections/stock_fund_flow_industry"
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
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "行业指数", "type": "float64", "description": "-"},
        {"name": "行业-涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "流入资金", "type": "float64", "description": "注意单位: 亿"},
        {"name": "流出资金", "type": "float64", "description": "注意单位: 亿"},
        {"name": "净额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "公司家数", "type": "float64", "description": "-"},
        {"name": "领涨股", "type": "object", "description": "-"},
        {"name": "领涨股-涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "当前价", "type": "float64", "description": "-"},
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "公司家数", "type": "int64", "description": "-"},
        {"name": "行业指数", "type": "float64", "description": "-"},
        {"name": "阶段涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "流入资金", "type": "float64", "description": "注意单位: 亿"},
        {"name": "流出资金", "type": "float64", "description": "注意单位: 亿"},
        {"name": "净额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
