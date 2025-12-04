"""
停复牌信息数据提供者

东方财富网-数据中心-特色数据-停复牌信息
接口: stock_tfp_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockTfpEmProvider(BaseProvider):
    """停复牌信息数据提供者"""
    
    # 必填属性
    collection_name = "stock_tfp_em"
    display_name = "停复牌信息"
    akshare_func = "stock_tfp_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-停复牌信息"
    collection_route = "/stocks/collections/stock_tfp_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "停牌时间", "type": "object", "description": "-"},
        {"name": "停牌截止时间", "type": "object", "description": "-"},
        {"name": "停牌期限", "type": "object", "description": "-"},
        {"name": "停牌原因", "type": "object", "description": "-"},
        {"name": "所属市场", "type": "object", "description": "-"},
        {"name": "预计复牌时间", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
