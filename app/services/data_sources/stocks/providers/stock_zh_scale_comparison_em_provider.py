"""
公司规模数据提供者

东方财富-行情中心-同行比较-公司规模
接口: stock_zh_scale_comparison_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhScaleComparisonEmProvider(BaseProvider):
    """公司规模数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_scale_comparison_em"
    display_name = "公司规模"
    akshare_func = "stock_zh_scale_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情中心-同行比较-公司规模"
    collection_route = "/stocks/collections/stock_zh_scale_comparison_em"
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
        {"name": "总市值", "type": "float64", "description": "-"},
        {"name": "总市值排名", "type": "int64", "description": "-"},
        {"name": "流通市值", "type": "float64", "description": "-"},
        {"name": "流通市值排名", "type": "int64", "description": "-"},
        {"name": "营业收入", "type": "float64", "description": "-"},
        {"name": "营业收入排名", "type": "int64", "description": "-"},
        {"name": "净利润", "type": "float64", "description": "-"},
        {"name": "净利润排名", "type": "int64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
