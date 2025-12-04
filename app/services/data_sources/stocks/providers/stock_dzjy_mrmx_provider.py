"""
每日明细数据提供者

东方财富网-数据中心-大宗交易-每日明细
接口: stock_dzjy_mrmx
"""
from app.services.data_sources.base_provider import BaseProvider


class StockDzjyMrmxProvider(BaseProvider):
    """每日明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_dzjy_mrmx"
    display_name = "每日明细"
    akshare_func = "stock_dzjy_mrmx"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-大宗交易-每日明细"
    collection_route = "/stocks/collections/stock_dzjy_mrmx"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "成交价", "type": "float64", "description": "-"},
        {"name": "折溢率", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "成交额/流通市值", "type": "float64", "description": "注意单位: %"},
        {"name": "买方营业部", "type": "object", "description": "-"},
        {"name": "卖方营业部", "type": "object", "description": "-"},
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "成交价", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "买方营业部", "type": "object", "description": "-"},
        {"name": "卖方营业部", "type": "object", "description": "-"},
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "成交价", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "买方营业部", "type": "object", "description": "-"},
        {"name": "卖方营业部", "type": "object", "description": "-"},
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "成交价", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "买方营业部", "type": "object", "description": "-"},
        {"name": "卖方营业部", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
