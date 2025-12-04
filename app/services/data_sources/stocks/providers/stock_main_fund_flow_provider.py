"""
主力净流入排名数据提供者

东方财富网-数据中心-资金流向-主力净流入排名
接口: stock_main_fund_flow
"""
from app.services.data_sources.base_provider import BaseProvider


class StockMainFundFlowProvider(BaseProvider):
    """主力净流入排名数据提供者"""
    
    # 必填属性
    collection_name = "stock_main_fund_flow"
    display_name = "主力净流入排名"
    akshare_func = "stock_main_fund_flow"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-主力净流入排名"
    collection_route = "/stocks/collections/stock_main_fund_flow"
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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "今日排行榜-主力净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日排行榜-今日排名", "type": "float64", "description": "-"},
        {"name": "今日排行榜-今日涨跌", "type": "float64", "description": "注意单位: %"},
        {"name": "5日排行榜-主力净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "5日排行榜-5日排名", "type": "int64", "description": "-"},
        {"name": "5日排行榜-5日涨跌", "type": "float64", "description": "注意单位: %"},
        {"name": "10日排行榜-主力净占比", "type": "float64", "description": "注意单位: %"},
        {"name": "10日排行榜-10日排名", "type": "int64", "description": "-"},
        {"name": "10日排行榜-10日涨跌", "type": "float64", "description": "注意单位: %"},
        {"name": "所属板块", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
