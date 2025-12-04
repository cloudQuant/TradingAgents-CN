"""
历史分红数据提供者

新浪财经-发行与分配-历史分红
接口: stock_history_dividend
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHistoryDividendProvider(SimpleProvider):
    """历史分红数据提供者"""
    
    # 必填属性
    collection_name = "stock_history_dividend"
    display_name = "历史分红"
    akshare_func = "stock_history_dividend"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-发行与分配-历史分红"
    collection_route = "/stocks/collections/stock_history_dividend"
    collection_category = "历史行情"

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "累计股息", "type": "float64", "description": "注意单位: %"},
        {"name": "年均股息", "type": "float64", "description": "注意单位: %"},
        {"name": "分红次数", "type": "float64", "description": "-"},
        {"name": "融资总额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "融资次数", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
