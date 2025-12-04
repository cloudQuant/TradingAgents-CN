"""
板块资金流排名数据提供者

东方财富网-数据中心-资金流向-板块资金流-排名
接口: stock_sector_fund_flow_rank
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSectorFundFlowRankProvider(BaseProvider):
    """板块资金流排名数据提供者"""
    
    # 必填属性
    collection_name = "stock_sector_fund_flow_rank"
    display_name = "板块资金流排名"
    akshare_func = "stock_sector_fund_flow_rank"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-板块资金流-排名"
    collection_route = "/stocks/collections/stock_sector_fund_flow_rank"
    collection_category = "板块数据"

    # 参数映射
    param_mapping = {
        "indicator": "indicator",
        "sector_type": "sector_type"
    }
    
    # 必填参数
    required_params = ['indicator', 'sector_type']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "今日涨跌幅", "type": "float64", "description": "注意单位: %"},
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
        {"name": "主力净流入最大股", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
