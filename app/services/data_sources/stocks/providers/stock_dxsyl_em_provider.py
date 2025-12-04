"""
打新收益率数据提供者

东方财富网-数据中心-新股申购-打新收益率
接口: stock_dxsyl_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockDxsylEmProvider(SimpleProvider):
    """打新收益率数据提供者"""
    
    # 必填属性
    collection_name = "stock_dxsyl_em"
    display_name = "打新收益率"
    akshare_func = "stock_dxsyl_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股申购-打新收益率"
    collection_route = "/stocks/collections/stock_dxsyl_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "发行价", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "网上发行中签率", "type": "float64", "description": "注意单位: %"},
        {"name": "网上有效申购股数", "type": "int64", "description": "-"},
        {"name": "网上有效申购户数", "type": "int64", "description": "注意单位: 户"},
        {"name": "网上超额认购倍数", "type": "float64", "description": "-"},
        {"name": "网下配售中签率", "type": "float64", "description": "注意单位: %"},
        {"name": "网下有效申购股数", "type": "int64", "description": "-"},
        {"name": "网下有效申购户数", "type": "int64", "description": "注意单位: 户"},
        {"name": "网下配售认购倍数", "type": "float64", "description": "-"},
        {"name": "总发行数量", "type": "int64", "description": "-"},
        {"name": "开盘溢价", "type": "float64", "description": "-"},
        {"name": "首日涨幅", "type": "float64", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
