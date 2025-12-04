"""
龙虎榜-营业部排行-上榜次数最多数据提供者

龙虎榜-营业部排行-上榜次数最多
接口: stock_lh_yyb_most
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockLhYybMostProvider(SimpleProvider):
    """龙虎榜-营业部排行-上榜次数最多数据提供者"""
    
    # 必填属性
    collection_name = "stock_lh_yyb_most"
    display_name = "龙虎榜-营业部排行-上榜次数最多"
    akshare_func = "stock_lh_yyb_most"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "龙虎榜-营业部排行-上榜次数最多"
    collection_route = "/stocks/collections/stock_lh_yyb_most"
    collection_category = "龙虎榜"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "上榜次数", "type": "int64", "description": "-"},
        {"name": "合计动用资金", "type": "object", "description": "-"},
        {"name": "年内上榜次数", "type": "int64", "description": "-"},
        {"name": "年内买入股票只数", "type": "int64", "description": "-"},
        {"name": "年内3日跟买成功率", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
