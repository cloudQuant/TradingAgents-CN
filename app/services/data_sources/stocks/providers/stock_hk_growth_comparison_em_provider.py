"""
成长性对比数据提供者

东方财富-港股-行业对比-成长性对比
接口: stock_hk_growth_comparison_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkGrowthComparisonEmProvider(BaseProvider):
    """成长性对比数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_growth_comparison_em"
    display_name = "成长性对比"
    akshare_func = "stock_hk_growth_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-行业对比-成长性对比"
    collection_route = "/stocks/collections/stock_hk_growth_comparison_em"
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
        {"name": "基本每股收益同比增长率", "type": "float64", "description": "-"},
        {"name": "基本每股收益同比增长率排名", "type": "int64", "description": "-"},
        {"name": "营业收入同比增长率", "type": "float64", "description": "-"},
        {"name": "营业收入同比增长率排名", "type": "int64", "description": "-"},
        {"name": "营业利润率同比增长率", "type": "float64", "description": "-"},
        {"name": "营业利润率同比增长率排名", "type": "int64", "description": "-"},
        {"name": "基本每股收总资产同比增长率益同比增长率", "type": "float64", "description": "-"},
        {"name": "总资产同比增长率排名", "type": "int64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
