"""
机构持股详情数据提供者

新浪财经-机构持股-机构持股详情
接口: stock_institute_hold_detail
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInstituteHoldDetailProvider(BaseProvider):
    """机构持股详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_institute_hold_detail"
    display_name = "机构持股详情"
    akshare_func = "stock_institute_hold_detail"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-机构持股-机构持股详情"
    collection_route = "/stocks/collections/stock_institute_hold_detail"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "stock": "stock",
        "quarter": "quarter"
    }
    
    # 必填参数
    required_params = ['stock', 'quarter']

    # 字段信息
    field_info = [
        {"name": "持股机构类型", "type": "object", "description": "-"},
        {"name": "持股机构代码", "type": "object", "description": "-"},
        {"name": "持股机构简称", "type": "object", "description": "-"},
        {"name": "持股机构全称", "type": "object", "description": "-"},
        {"name": "持股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "最新持股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "持股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "最新持股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "最新占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "持股比例增幅", "type": "float64", "description": "注意单位: %"},
        {"name": "占流通股比例增幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
