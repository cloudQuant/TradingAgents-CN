"""
机构持股一览表数据提供者

新浪财经-机构持股-机构持股一览表
接口: stock_institute_hold
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInstituteHoldProvider(BaseProvider):
    """机构持股一览表数据提供者"""
    
    # 必填属性
    collection_name = "stock_institute_hold"
    display_name = "机构持股一览表"
    akshare_func = "stock_institute_hold"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-机构持股-机构持股一览表"
    collection_route = "/stocks/collections/stock_institute_hold"
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
        {"name": "机构数", "type": "int64", "description": "-"},
        {"name": "机构数变化", "type": "int64", "description": "-"},
        {"name": "持股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "持股比例增幅", "type": "float64", "description": "注意单位: %"},
        {"name": "占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "占流通股比例增幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
