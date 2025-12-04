"""
龙虎榜-营业部排行-资金实力最强数据提供者

龙虎榜-营业部排行-资金实力最强
接口: stock_lh_yyb_capital
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockLhYybCapitalProvider(SimpleProvider):
    """龙虎榜-营业部排行-资金实力最强数据提供者"""
    
    # 必填属性
    collection_name = "stock_lh_yyb_capital"
    display_name = "龙虎榜-营业部排行-资金实力最强"
    akshare_func = "stock_lh_yyb_capital"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "龙虎榜-营业部排行-资金实力最强"
    collection_route = "/stocks/collections/stock_lh_yyb_capital"
    collection_category = "资金流向"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "今日最高操作", "type": "int64", "description": "-"},
        {"name": "今日最高金额", "type": "object", "description": "-"},
        {"name": "今日最高买入金额", "type": "object", "description": "-"},
        {"name": "累计参与金额", "type": "object", "description": "-"},
        {"name": "累计买入金额", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
