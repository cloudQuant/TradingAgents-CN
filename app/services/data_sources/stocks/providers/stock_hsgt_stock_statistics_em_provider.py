"""
每日个股统计数据提供者

东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计
接口: stock_hsgt_stock_statistics_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtStockStatisticsEmProvider(BaseProvider):
    """每日个股统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_stock_statistics_em"
    display_name = "每日个股统计"
    akshare_func = "stock_hsgt_stock_statistics_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计"
    collection_route = "/stocks/collections/stock_hsgt_stock_statistics_em"
    collection_category = "沪深港通"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "持股日期", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "当日收盘价", "type": "float64", "description": "注意单位: 元; 南向持股单位为: 港元"},
        {"name": "当日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "持股数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 万元"},
        {"name": "持股数量占发行股百分比", "type": "float64", "description": "注意单位: %"},
        {"name": "持股市值变化-1日", "type": "float64", "description": "注意单位: 元"},
        {"name": "持股市值变化-5日", "type": "float64", "description": "注意单位: 元"},
        {"name": "持股市值变化-10日", "type": "float64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
