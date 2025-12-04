"""
筹码分布数据提供者

东方财富网-概念板-行情中心-日K-筹码分布
接口: stock_cyq_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCyqEmProvider(BaseProvider):
    """筹码分布数据提供者"""
    
    # 必填属性
    collection_name = "stock_cyq_em"
    display_name = "筹码分布"
    akshare_func = "stock_cyq_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-概念板-行情中心-日K-筹码分布"
    collection_route = "/stocks/collections/stock_cyq_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "获利比例", "type": "float64", "description": "-"},
        {"name": "平均成本", "type": "float64", "description": "-"},
        {"name": "90成本-低", "type": "float64", "description": "-"},
        {"name": "90成本-高", "type": "float64", "description": "-"},
        {"name": "90集中度", "type": "float64", "description": "-"},
        {"name": "70成本-低", "type": "float64", "description": "-"},
        {"name": "70成本-高", "type": "float64", "description": "-"},
        {"name": "70集中度", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
