"""
港股个股指标数据提供者

亿牛网-港股个股指标: 市盈率, 市净率, 股息率, ROE, 市值
接口: stock_hk_indicator_eniu
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkIndicatorEniuProvider(BaseProvider):
    """港股个股指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_indicator_eniu"
    display_name = "港股个股指标"
    akshare_func = "stock_hk_indicator_eniu"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "亿牛网-港股个股指标: 市盈率, 市净率, 股息率, ROE, 市值"
    collection_route = "/stocks/collections/stock_hk_indicator_eniu"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "-", "type": "-", "description": "根据 indicator 而异"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
