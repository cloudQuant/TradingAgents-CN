"""
港股估值指标数据提供者

百度股市通-港股-财务报表-估值数据
接口: stock_hk_valuation_baidu
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkValuationBaiduProvider(BaseProvider):
    """港股估值指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_valuation_baidu"
    display_name = "港股估值指标"
    akshare_func = "stock_hk_valuation_baidu"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "百度股市通-港股-财务报表-估值数据"
    collection_route = "/stocks/collections/stock_hk_valuation_baidu"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator",
        "period": "period"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator', 'period']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "-"},
        {"name": "value", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
