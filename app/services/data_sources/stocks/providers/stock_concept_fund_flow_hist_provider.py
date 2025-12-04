"""
概念历史资金流数据提供者

东方财富网-数据中心-资金流向-概念资金流-概念历史资金流
接口: stock_concept_fund_flow_hist
"""
from app.services.data_sources.base_provider import BaseProvider


class StockConceptFundFlowHistProvider(BaseProvider):
    """概念历史资金流数据提供者"""
    
    # 必填属性
    collection_name = "stock_concept_fund_flow_hist"
    display_name = "概念历史资金流"
    akshare_func = "stock_concept_fund_flow_hist"
    unique_keys = ['日期']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-概念资金流-概念历史资金流"
    collection_route = "/stocks/collections/stock_concept_fund_flow_hist"
    collection_category = "历史行情"

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
        {"name": "日期", "type": "object", "description": "注意单位: %"},
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
