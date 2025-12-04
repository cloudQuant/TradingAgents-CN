"""
个股排行数据提供者

东方财富网-数据中心-沪深港通持股-个股排行
接口: stock_hsgt_hold_stock_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtHoldStockEmProvider(BaseProvider):
    """个股排行数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_hold_stock_em"
    display_name = "个股排行"
    akshare_func = "stock_hsgt_hold_stock_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-沪深港通持股-个股排行"
    collection_route = "/stocks/collections/stock_hsgt_hold_stock_em"
    collection_category = "沪深港通"

    # 参数映射
    param_mapping = {
        "market": "market",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['market', 'indicator']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "今日收盘价", "type": "float64", "description": "-"},
        {"name": "今日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "今日持股-股数", "type": "float64", "description": "注意单位: 万"},
        {"name": "今日持股-市值", "type": "float64", "description": "注意单位: 万"},
        {"name": "今日持股-占流通股比", "type": "float64", "description": "注意单位: %"},
        {"name": "今日持股-占总股本比", "type": "float64", "description": "注意单位: %"},
        {"name": "增持估计-股数", "type": "float64", "description": "注意单位: 万; 主要字段名根据 indicator 变化"},
        {"name": "增持估计-市值", "type": "float64", "description": "注意单位: 万; 主要字段名根据 indicator 变化"},
        {"name": "增持估计-市值增幅", "type": "object", "description": "注意单位: %; 主要字段名根据 indicator 变化"},
        {"name": "增持估计-占流通股比", "type": "float64", "description": "注意单位: ‰; 主要字段名根据 indicator 变化"},
        {"name": "增持估计-占总股本比", "type": "float64", "description": "注意单位: ‰; 主要字段名根据 indicator 变化"},
        {"name": "所属板块", "type": "object", "description": "-"},
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
