"""
板块异动详情数据提供者

东方财富-行情中心-当日板块异动详情
接口: stock_board_change_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBoardChangeEmProvider(SimpleProvider):
    """板块异动详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_change_em"
    display_name = "板块异动详情"
    akshare_func = "stock_board_change_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情中心-当日板块异动详情"
    collection_route = "/stocks/collections/stock_board_change_em"
    collection_category = "板块数据"

    # 字段信息
    field_info = [
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "主力净流入", "type": "float64", "description": "注意单位: 万元"},
        {"name": "板块异动总次数", "type": "float64", "description": "-"},
        {"name": "板块异动最频繁个股及所属类型-股票代码", "type": "object", "description": "-"},
        {"name": "板块异动最频繁个股及所属类型-买卖方向", "type": "object", "description": "-"},
        {"name": "板块具体异动类型列表及出现次数", "type": "object", "description": "返回具体异动的字典"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
