"""
股票账户统计月度数据提供者

东方财富网-数据中心-特色数据-股票账户统计
接口: stock_account_statistics_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockAccountStatisticsEmProvider(SimpleProvider):
    """股票账户统计月度数据提供者"""
    
    # 必填属性
    collection_name = "stock_account_statistics_em"
    display_name = "股票账户统计月度"
    akshare_func = "stock_account_statistics_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股票账户统计"
    collection_route = "/stocks/collections/stock_account_statistics_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "数据日期", "type": "object", "description": "-"},
        {"name": "新增投资者-数量", "type": "float64", "description": "注意单位: 万户"},
        {"name": "新增投资者-环比", "type": "float64", "description": "-"},
        {"name": "新增投资者-同比", "type": "float64", "description": "-"},
        {"name": "期末投资者-总量", "type": "float64", "description": "注意单位: 万户"},
        {"name": "期末投资者-A股账户", "type": "float64", "description": "注意单位: 万户"},
        {"name": "期末投资者-B股账户", "type": "float64", "description": "注意单位: 万户"},
        {"name": "沪深总市值", "type": "float64", "description": "-"},
        {"name": "沪深户均市值", "type": "float64", "description": "注意单位: 万"},
        {"name": "上证指数-收盘", "type": "float64", "description": "-"},
        {"name": "上证指数-涨跌幅", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
