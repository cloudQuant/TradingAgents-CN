"""
股东协同-十大流通股东数据提供者

东方财富网-数据中心-股东分析-股东协同-十大流通股东
接口: stock_gdfx_free_holding_teamwork_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGdfxFreeHoldingTeamworkEmProvider(BaseProvider):
    """股东协同-十大流通股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_gdfx_free_holding_teamwork_em"
    display_name = "股东协同-十大流通股东"
    akshare_func = "stock_gdfx_free_holding_teamwork_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股东分析-股东协同-十大流通股东"
    collection_route = "/stocks/collections/stock_gdfx_free_holding_teamwork_em"
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
        {"name": "股东类型", "type": "object", "description": "-"},
        {"name": "协同股东类型", "type": "object", "description": "-"},
        {"name": "协同次数", "type": "int64", "description": "-"},
        {"name": "个股详情", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
