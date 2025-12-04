"""
龙虎榜-营业部排行-抱团操作实力数据提供者

龙虎榜-营业部排行-抱团操作实力
接口: stock_lh_yyb_control
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockLhYybControlProvider(SimpleProvider):
    """龙虎榜-营业部排行-抱团操作实力数据提供者"""
    
    # 必填属性
    collection_name = "stock_lh_yyb_control"
    display_name = "龙虎榜-营业部排行-抱团操作实力"
    akshare_func = "stock_lh_yyb_control"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "龙虎榜-营业部排行-抱团操作实力"
    collection_route = "/stocks/collections/stock_lh_yyb_control"
    collection_category = "龙虎榜"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "携手营业部家数", "type": "int64", "description": "-"},
        {"name": "年内最佳携手对象", "type": "object", "description": "-"},
        {"name": "年内最佳携手股票数", "type": "int64", "description": "-"},
        {"name": "年内最佳携手成功率", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
