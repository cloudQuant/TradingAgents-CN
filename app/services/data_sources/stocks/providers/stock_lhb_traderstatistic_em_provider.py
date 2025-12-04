"""
营业部统计数据提供者

东方财富网-数据中心-龙虎榜单-营业部统计
接口: stock_lhb_traderstatistic_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbTraderstatisticEmProvider(BaseProvider):
    """营业部统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_traderstatistic_em"
    display_name = "营业部统计"
    akshare_func = "stock_lhb_traderstatistic_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-营业部统计"
    collection_route = "/stocks/collections/stock_lhb_traderstatistic_em"
    collection_category = "龙虎榜"

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
        {"name": "龙虎榜成交金额", "type": "float64", "description": "-"},
        {"name": "上榜次数", "type": "int64", "description": "-"},
        {"name": "买入额", "type": "float64", "description": "注意单位: 元"},
        {"name": "买入次数", "type": "int64", "description": "-"},
        {"name": "卖出额", "type": "float64", "description": "注意单位: 元"},
        {"name": "卖出次数", "type": "int64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
