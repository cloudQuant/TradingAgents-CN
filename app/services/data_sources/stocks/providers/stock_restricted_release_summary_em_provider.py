"""
限售股解禁数据提供者

东方财富网-数据中心-特色数据-限售股解禁
接口: stock_restricted_release_summary_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRestrictedReleaseSummaryEmProvider(BaseProvider):
    """限售股解禁数据提供者"""
    
    # 必填属性
    collection_name = "stock_restricted_release_summary_em"
    display_name = "限售股解禁"
    akshare_func = "stock_restricted_release_summary_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-限售股解禁"
    collection_route = "/stocks/collections/stock_restricted_release_summary_em"
    collection_category = "默认"

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "解禁时间", "type": "object", "description": "-"},
        {"name": "当日解禁股票家数", "type": "int64", "description": "-"},
        {"name": "解禁数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "实际解禁数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "实际解禁市值", "type": "int64", "description": "注意单位: 元"},
        {"name": "沪深300指数", "type": "float64", "description": "-"},
        {"name": "沪深300指数涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
