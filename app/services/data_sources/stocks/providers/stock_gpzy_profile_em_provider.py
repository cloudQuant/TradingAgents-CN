"""
股权质押市场概况数据提供者

东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
接口: stock_gpzy_profile_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockGpzyProfileEmProvider(SimpleProvider):
    """股权质押市场概况数据提供者"""
    
    # 必填属性
    collection_name = "stock_gpzy_profile_em"
    display_name = "股权质押市场概况"
    akshare_func = "stock_gpzy_profile_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股权质押-股权质押市场概况"
    collection_route = "/stocks/collections/stock_gpzy_profile_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "A股质押总比例", "type": "float64", "description": "注意单位: %"},
        {"name": "质押公司数量", "type": "float64", "description": "-"},
        {"name": "质押笔数", "type": "float64", "description": "注意单位: 笔"},
        {"name": "质押总股数", "type": "float64", "description": "注意单位: 股"},
        {"name": "质押总市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "沪深300指数", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
