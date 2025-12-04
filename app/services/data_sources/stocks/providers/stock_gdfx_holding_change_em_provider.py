"""
股东持股变动统计-十大股东数据提供者

东方财富网-数据中心-股东分析-股东持股变动统计-十大股东
接口: stock_gdfx_holding_change_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGdfxHoldingChangeEmProvider(BaseProvider):
    """股东持股变动统计-十大股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_gdfx_holding_change_em"
    display_name = "股东持股变动统计-十大股东"
    akshare_func = "stock_gdfx_holding_change_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股东分析-股东持股变动统计-十大股东"
    collection_route = "/stocks/collections/stock_gdfx_holding_change_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股东类型", "type": "object", "description": "-"},
        {"name": "期末持股只数统计-总持有", "type": "float64", "description": "-"},
        {"name": "期末持股只数统计-新进", "type": "float64", "description": "-"},
        {"name": "期末持股只数统计-增加", "type": "float64", "description": "-"},
        {"name": "期末持股只数统计-不变", "type": "float64", "description": "-"},
        {"name": "期末持股只数统计-减少", "type": "float64", "description": "-"},
        {"name": "流通市值统计", "type": "float64", "description": "注意单位: 元"},
        {"name": "持有个股", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
