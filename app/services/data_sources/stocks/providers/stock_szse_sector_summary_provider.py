"""
股票行业成交数据提供者

深圳证券交易所-统计资料-股票行业成交数据
接口: stock_szse_sector_summary
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSzseSectorSummaryProvider(BaseProvider):
    """股票行业成交数据提供者"""
    
    # 必填属性
    collection_name = "stock_szse_sector_summary"
    display_name = "股票行业成交"
    akshare_func = "stock_szse_sector_summary"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深圳证券交易所-统计资料-股票行业成交数据"
    collection_route = "/stocks/collections/stock_szse_sector_summary"
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
        {"name": "交易天数", "type": "int64", "description": "-"},
        {"name": "成交金额-人民币元", "type": "int64", "description": "-"},
        {"name": "成交金额-占总计", "type": "float64", "description": "注意单位: %"},
        {"name": "成交股数-股数", "type": "int64", "description": "-"},
        {"name": "成交股数-占总计", "type": "float64", "description": "注意单位: %"},
        {"name": "成交笔数-笔", "type": "int64", "description": "-"},
        {"name": "成交笔数-占总计", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
