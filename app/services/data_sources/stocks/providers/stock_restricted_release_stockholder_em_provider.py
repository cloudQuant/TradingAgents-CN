"""
解禁股东数据提供者

东方财富网-数据中心-个股限售解禁-解禁股东
接口: stock_restricted_release_stockholder_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRestrictedReleaseStockholderEmProvider(BaseProvider):
    """解禁股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_restricted_release_stockholder_em"
    display_name = "解禁股东"
    akshare_func = "stock_restricted_release_stockholder_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-个股限售解禁-解禁股东"
    collection_route = "/stocks/collections/stock_restricted_release_stockholder_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "解禁数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "实际解禁数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "解禁市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "锁定期", "type": "int64", "description": "注意单位: 月"},
        {"name": "剩余未解禁数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "限售股类型", "type": "object", "description": "-"},
        {"name": "进度", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
