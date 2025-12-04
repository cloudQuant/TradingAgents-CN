"""
实际控制人持股变动数据提供者

巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动
接口: stock_hold_control_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHoldControlCninfoProvider(BaseProvider):
    """实际控制人持股变动数据提供者"""
    
    # 必填属性
    collection_name = "stock_hold_control_cninfo"
    display_name = "实际控制人持股变动"
    akshare_func = "stock_hold_control_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动"
    collection_route = "/stocks/collections/stock_hold_control_cninfo"
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
        {"name": "证劵代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "控股数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "控股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "控制类型", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
