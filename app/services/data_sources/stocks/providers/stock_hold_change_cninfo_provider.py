"""
股本变动数据提供者

巨潮资讯-数据中心-专题统计-股东股本-股本变动
接口: stock_hold_change_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHoldChangeCninfoProvider(BaseProvider):
    """股本变动数据提供者"""
    
    # 必填属性
    collection_name = "stock_hold_change_cninfo"
    display_name = "股本变动"
    akshare_func = "stock_hold_change_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-专题统计-股东股本-股本变动"
    collection_route = "/stocks/collections/stock_hold_change_cninfo"
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
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "交易市场", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "总股本", "type": "float64", "description": "单位: 万股"},
        {"name": "已流通股份", "type": "float64", "description": "单位: 万股"},
        {"name": "已流通比例", "type": "float64", "description": "单位: %"},
        {"name": "流通受限股份", "type": "float64", "description": "单位: 万股"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
