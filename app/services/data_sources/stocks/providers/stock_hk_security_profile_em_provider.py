"""
证券资料数据提供者

东方财富-港股-证券资料
接口: stock_hk_security_profile_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkSecurityProfileEmProvider(BaseProvider):
    """证券资料数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_security_profile_em"
    display_name = "证券资料"
    akshare_func = "stock_hk_security_profile_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-证券资料"
    collection_route = "/stocks/collections/stock_hk_security_profile_em"
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
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "证券类型", "type": "object", "description": "-"},
        {"name": "发行价", "type": "float64", "description": "-"},
        {"name": "发行量(股)", "type": "int64", "description": "-"},
        {"name": "每手股数", "type": "int64", "description": "-"},
        {"name": "每股面值", "type": "object", "description": "-"},
        {"name": "交易所", "type": "object", "description": "-"},
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "年结日", "type": "object", "description": "-"},
        {"name": "ISIN（国际证券识别编码）", "type": "object", "description": "-"},
        {"name": "是否沪港通标的", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
