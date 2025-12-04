"""
股东人数及持股集中度数据提供者

巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度
接口: stock_hold_num_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHoldNumCninfoProvider(BaseProvider):
    """股东人数及持股集中度数据提供者"""
    
    # 必填属性
    collection_name = "stock_hold_num_cninfo"
    display_name = "股东人数及持股集中度"
    akshare_func = "stock_hold_num_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度"
    collection_route = "/stocks/collections/stock_hold_num_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "证劵代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "本期股东人数", "type": "int64", "description": "-"},
        {"name": "上期股东人数", "type": "float64", "description": "-"},
        {"name": "股东人数增幅", "type": "float64", "description": "注意单位: %"},
        {"name": "本期人均持股数量", "type": "int64", "description": "注意单位: 万股"},
        {"name": "上期人均持股数量", "type": "float64", "description": "注意单位: %"},
        {"name": "人均持股数量增幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
