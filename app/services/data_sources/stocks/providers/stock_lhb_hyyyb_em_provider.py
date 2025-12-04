"""
每日活跃营业部数据提供者

东方财富网-数据中心-龙虎榜单-每日活跃营业部
接口: stock_lhb_hyyyb_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbHyyybEmProvider(BaseProvider):
    """每日活跃营业部数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_hyyyb_em"
    display_name = "每日活跃营业部"
    akshare_func = "stock_lhb_hyyyb_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-每日活跃营业部"
    collection_route = "/stocks/collections/stock_lhb_hyyyb_em"
    collection_category = "龙虎榜"

    # 参数映射
    param_mapping = {
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "上榜日", "type": "object", "description": "-"},
        {"name": "买入个股数", "type": "float64", "description": "-"},
        {"name": "卖出个股数", "type": "float64", "description": "-"},
        {"name": "买入总金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "卖出总金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "总买卖净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "买入股票", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
