"""
分红派息数据提供者

东方财富-港股-核心必读-分红派息
接口: stock_hk_dividend_payout_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkDividendPayoutEmProvider(BaseProvider):
    """分红派息数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_dividend_payout_em"
    display_name = "分红派息"
    akshare_func = "stock_hk_dividend_payout_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-核心必读-分红派息"
    collection_route = "/stocks/collections/stock_hk_dividend_payout_em"
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
        {"name": "最新公告日期", "type": "object", "description": "-"},
        {"name": "财政年度", "type": "object", "description": "-"},
        {"name": "分红方案", "type": "object", "description": "-"},
        {"name": "分配类型", "type": "object", "description": "-"},
        {"name": "除净日", "type": "object", "description": "-"},
        {"name": "截至过户日", "type": "object", "description": "-"},
        {"name": "发放日", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
