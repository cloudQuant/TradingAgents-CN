"""
股票回购数据数据提供者

东方财富网-数据中心-股票回购-股票回购数据
接口: stock_repurchase_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockRepurchaseEmProvider(SimpleProvider):
    """股票回购数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_repurchase_em"
    display_name = "股票回购数据"
    akshare_func = "stock_repurchase_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股票回购-股票回购数据"
    collection_route = "/stocks/collections/stock_repurchase_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "计划回购价格区间", "type": "float64", "description": "注意单位: 元"},
        {"name": "计划回购数量区间-下限", "type": "float64", "description": "注意单位: 股"},
        {"name": "计划回购数量区间-上限", "type": "float64", "description": "注意单位: 股"},
        {"name": "占公告前一日总股本比例-下限", "type": "float64", "description": "注意单位: %"},
        {"name": "占公告前一日总股本比例-上限", "type": "float64", "description": "注意单位: %"},
        {"name": "计划回购金额区间-下限", "type": "float64", "description": "注意单位: 元"},
        {"name": "计划回购金额区间-上限", "type": "float64", "description": "注意单位: 元"},
        {"name": "回购起始时间", "type": "object", "description": "-"},
        {"name": "实施进度", "type": "object", "description": "-"},
        {"name": "已回购股份价格区间-下限", "type": "float64", "description": "注意单位: %"},
        {"name": "已回购股份价格区间-上限", "type": "float64", "description": "注意单位: %"},
        {"name": "已回购股份数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "已回购金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "最新公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
