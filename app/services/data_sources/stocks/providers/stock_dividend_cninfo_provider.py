"""
历史分红数据提供者

巨潮资讯-个股-历史分红
接口: stock_dividend_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockDividendCninfoProvider(BaseProvider):
    """历史分红数据提供者"""
    
    # 必填属性
    collection_name = "stock_dividend_cninfo"
    display_name = "历史分红"
    akshare_func = "stock_dividend_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-个股-历史分红"
    collection_route = "/stocks/collections/stock_dividend_cninfo"
    collection_category = "历史行情"

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
        {"name": "实施方案公告日期", "type": "object", "description": "-"},
        {"name": "送股比例", "type": "float64", "description": "注意单位: 每 10 股"},
        {"name": "转增比例", "type": "float64", "description": "注意单位: 每 10 股"},
        {"name": "派息比例", "type": "float64", "description": "注意单位: 每 10 股"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "除权日", "type": "object", "description": "-"},
        {"name": "派息日", "type": "object", "description": "-"},
        {"name": "股份到账日", "type": "object", "description": "-"},
        {"name": "实施方案分红说明", "type": "object", "description": "-"},
        {"name": "分红类型", "type": "object", "description": "-"},
        {"name": "报告时间", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
