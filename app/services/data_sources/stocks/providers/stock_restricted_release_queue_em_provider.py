"""
解禁批次数据提供者

东方财富网-数据中心-个股限售解禁-解禁批次
接口: stock_restricted_release_queue_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRestrictedReleaseQueueEmProvider(BaseProvider):
    """解禁批次数据提供者"""
    
    # 必填属性
    collection_name = "stock_restricted_release_queue_em"
    display_name = "解禁批次"
    akshare_func = "stock_restricted_release_queue_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-个股限售解禁-解禁批次"
    collection_route = "/stocks/collections/stock_restricted_release_queue_em"
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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "解禁时间", "type": "object", "description": "-"},
        {"name": "解禁股东数", "type": "int64", "description": "-"},
        {"name": "解禁数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "实际解禁数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "未解禁数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "实际解禁数量市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "占总市值比例", "type": "float64", "description": "-"},
        {"name": "占流通市值比例", "type": "float64", "description": "-"},
        {"name": "解禁前一交易日收盘价", "type": "float64", "description": "注意单位: 元"},
        {"name": "限售股类型", "type": "object", "description": "-"},
        {"name": "解禁前20日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "解禁后20日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
