"""
个股龙虎榜详情数据提供者

东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
接口: stock_lhb_stock_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbStockDetailEmProvider(BaseProvider):
    """个股龙虎榜详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_stock_detail_em"
    display_name = "个股龙虎榜详情"
    akshare_func = "stock_lhb_stock_detail_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-个股龙虎榜详情"
    collection_route = "/stocks/collections/stock_lhb_stock_detail_em"
    collection_category = "龙虎榜"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date",
        "flag": "flag"
    }
    
    # 必填参数
    required_params = ['symbol', 'date', 'flag']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "买入金额", "type": "float64", "description": "-"},
        {"name": "买入金额-占总成交比例", "type": "float64", "description": "-"},
        {"name": "卖出金额-占总成交比例", "type": "float64", "description": "-"},
        {"name": "净额", "type": "float64", "description": "-"},
        {"name": "类型", "type": "object", "description": "该字段主要处理多种龙虎榜标准问题"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
