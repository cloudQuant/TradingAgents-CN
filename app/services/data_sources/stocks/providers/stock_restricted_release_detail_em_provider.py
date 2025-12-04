"""
限售股解禁详情数据提供者

东方财富网-数据中心-限售股解禁-解禁详情一览
接口: stock_restricted_release_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRestrictedReleaseDetailEmProvider(BaseProvider):
    """限售股解禁详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_restricted_release_detail_em"
    display_name = "限售股解禁详情"
    akshare_func = "stock_restricted_release_detail_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-限售股解禁-解禁详情一览"
    collection_route = "/stocks/collections/stock_restricted_release_detail_em"
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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "解禁时间", "type": "object", "description": "-"},
        {"name": "限售股类型", "type": "object", "description": "注意单位: 股"},
        {"name": "解禁数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "实际解禁数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "实际解禁市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "占解禁前流通市值比例", "type": "float64", "description": "-"},
        {"name": "解禁前一交易日收盘价", "type": "float64", "description": "-"},
        {"name": "解禁前20日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "解禁后20日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
