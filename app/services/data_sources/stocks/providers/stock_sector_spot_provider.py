"""
板块行情数据提供者

新浪行业-板块行情
接口: stock_sector_spot
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSectorSpotProvider(BaseProvider):
    """板块行情数据提供者"""
    
    # 必填属性
    collection_name = "stock_sector_spot"
    display_name = "板块行情"
    akshare_func = "stock_sector_spot"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪行业-板块行情"
    collection_route = "/stocks/collections/stock_sector_spot"
    collection_category = "实时行情"

    # 参数映射
    param_mapping = {
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['indicator']

    # 字段信息
    field_info = [
        {"name": "label", "type": "object", "description": "-"},
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "公司家数", "type": "int64", "description": "-"},
        {"name": "平均价格", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "总成交量", "type": "int64", "description": "注意单位: 手"},
        {"name": "总成交额", "type": "int64", "description": "注意单位: 万元"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "个股-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "个股-当前价", "type": "float64", "description": "-"},
        {"name": "个股-涨跌额", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
