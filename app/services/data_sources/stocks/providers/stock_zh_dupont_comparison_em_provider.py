"""
杜邦分析比较数据提供者

东方财富-行情中心-同行比较-杜邦分析比较
接口: stock_zh_dupont_comparison_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhDupontComparisonEmProvider(BaseProvider):
    """杜邦分析比较数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_dupont_comparison_em"
    display_name = "杜邦分析比较"
    akshare_func = "stock_zh_dupont_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情中心-同行比较-杜邦分析比较"
    collection_route = "/stocks/collections/stock_zh_dupont_comparison_em"
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
        {"name": "ROE-3年平均", "type": "float64", "description": "-"},
        {"name": "ROE-22A", "type": "float64", "description": "-"},
        {"name": "ROE-23A", "type": "float64", "description": "-"},
        {"name": "ROE-24A", "type": "float64", "description": "-"},
        {"name": "净利率-3年平均", "type": "float64", "description": "-"},
        {"name": "净利率-22A", "type": "float64", "description": "-"},
        {"name": "净利率-23A", "type": "float64", "description": "-"},
        {"name": "净利率-24A", "type": "float64", "description": "-"},
        {"name": "总资产周转率-3年平均", "type": "float64", "description": "-"},
        {"name": "总资产周转率-22A", "type": "float64", "description": "-"},
        {"name": "总资产周转率-23A", "type": "float64", "description": "-"},
        {"name": "总资产周转率-24A", "type": "float64", "description": "-"},
        {"name": "权益乘数-3年平均", "type": "float64", "description": "-"},
        {"name": "权益乘数-22A", "type": "float64", "description": "-"},
        {"name": "权益乘数-23A", "type": "float64", "description": "-"},
        {"name": "权益乘数-24A", "type": "float64", "description": "-"},
        {"name": "ROE-3年平均排名", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
