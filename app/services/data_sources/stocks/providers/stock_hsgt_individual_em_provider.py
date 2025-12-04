"""
沪深港通持股-个股数据提供者

东方财富网-数据中心-沪深港通-沪深港通持股-具体股票
接口: stock_hsgt_individual_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtIndividualEmProvider(BaseProvider):
    """沪深港通持股-个股数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_individual_em"
    display_name = "沪深港通持股-个股"
    akshare_func = "stock_hsgt_individual_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-沪深港通-沪深港通持股-具体股票"
    collection_route = "/stocks/collections/stock_hsgt_individual_em"
    collection_category = "沪深港通"

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
        {"name": "持股日期", "type": "object", "description": "-"},
        {"name": "当日收盘价", "type": "float64", "description": "注意单位: 元"},
        {"name": "当日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "持股数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "持股数量占A股百分比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日增持股数", "type": "float64", "description": "注意单位: 股"},
        {"name": "今日增持资金", "type": "float64", "description": "注意单位: 元"},
        {"name": "今日持股市值变化", "type": "float64", "description": "注意单位: 元"},
        {"name": "持股日期", "type": "object", "description": "-"},
        {"name": "当日收盘价", "type": "float64", "description": "注意单位: 港元"},
        {"name": "当日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "持股数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 港元"},
        {"name": "持股数量占A股百分比", "type": "float64", "description": "注意单位: %"},
        {"name": "持股市值变化-1日", "type": "float64", "description": "注意单位: 港元"},
        {"name": "持股市值变化-5日", "type": "float64", "description": "注意单位: 港元"},
        {"name": "持股市值变化-10日", "type": "float64", "description": "注意单位: 港元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
