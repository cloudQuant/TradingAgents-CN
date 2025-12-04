"""
每日统计数据提供者

东方财富网-数据中心-大宗交易-每日统计
接口: stock_dzjy_mrtj
"""
from app.services.data_sources.base_provider import BaseProvider


class StockDzjyMrtjProvider(BaseProvider):
    """每日统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_dzjy_mrtj"
    display_name = "每日统计"
    akshare_func = "stock_dzjy_mrtj"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-大宗交易-每日统计"
    collection_route = "/stocks/collections/stock_dzjy_mrtj"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "成交均价", "type": "float64", "description": "-"},
        {"name": "折溢率", "type": "float64", "description": "-"},
        {"name": "成交笔数", "type": "int64", "description": "-"},
        {"name": "成交总量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "成交总额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "成交总额/流通市值", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
