"""
成长性比较数据提供者

东方财富-行情中心-同行比较-成长性比较
接口: stock_zh_growth_comparison_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhGrowthComparisonEmProvider(BaseProvider):
    """成长性比较数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_growth_comparison_em"
    display_name = "成长性比较"
    akshare_func = "stock_zh_growth_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情中心-同行比较-成长性比较"
    collection_route = "/stocks/collections/stock_zh_growth_comparison_em"
    collection_category = "默认"

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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "基本每股收益增长率-3年复合", "type": "float64", "description": "-"},
        {"name": "基本每股收益增长率-24A", "type": "float64", "description": "-"},
        {"name": "基本每股收益增长率-TTM", "type": "float64", "description": "-"},
        {"name": "基本每股收益增长率-25E", "type": "float64", "description": "-"},
        {"name": "基本每股收益增长率-26E", "type": "float64", "description": "-"},
        {"name": "基本每股收益增长率-27E", "type": "float64", "description": "-"},
        {"name": "营业收入增长率-3年复合", "type": "float64", "description": "-"},
        {"name": "营业收入增长率-24A", "type": "float64", "description": "-"},
        {"name": "营业收入增长率-TTM", "type": "float64", "description": "-"},
        {"name": "营业收入增长率-25E", "type": "float64", "description": "-"},
        {"name": "营业收入增长率-26E", "type": "float64", "description": "-"},
        {"name": "营业收入增长率-27E", "type": "float64", "description": "-"},
        {"name": "净利润增长率-3年复合", "type": "float64", "description": "-"},
        {"name": "净利润增长率-24A", "type": "float64", "description": "-"},
        {"name": "净利润增长率-TTM", "type": "float64", "description": "-"},
        {"name": "净利润增长率-25E", "type": "float64", "description": "-"},
        {"name": "净利润增长率-26E", "type": "float64", "description": "-"},
        {"name": "净利润增长率-27E", "type": "float64", "description": "-"},
        {"name": "基本每股收益增长率-3年复合排名", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
