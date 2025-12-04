"""
港股主板实时行情数据-东财数据提供者

港股主板的实时行情数据; 该数据有 15 分钟延时
接口: stock_hk_main_board_spot_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkMainBoardSpotEmProvider(SimpleProvider):
    """港股主板实时行情数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_main_board_spot_em"
    display_name = "港股主板实时行情数据-东财"
    akshare_func = "stock_hk_main_board_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "港股主板的实时行情数据; 该数据有 15 分钟延时"
    collection_route = "/stocks/collections/stock_hk_main_board_spot_em"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 港元"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
