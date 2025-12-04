"""
实时行情数据数据提供者

新浪财经-科创板股票实时行情数据
接口: stock_zh_kcb_spot
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhKcbSpotProvider(SimpleProvider):
    """实时行情数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_kcb_spot"
    display_name = "实时行情数据"
    akshare_func = "stock_zh_kcb_spot"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-科创板股票实时行情数据"
    collection_route = "/stocks/collections/stock_zh_kcb_spot"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "买入", "type": "float64", "description": "-"},
        {"name": "卖出", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "时点", "type": "object", "description": "注意: 数据获取的时间点"},
        {"name": "市盈率", "type": "float64", "description": "-"},
        {"name": "市净率", "type": "float64", "description": "-"},
        {"name": "流通市值", "type": "float64", "description": "-"},
        {"name": "总市值", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
