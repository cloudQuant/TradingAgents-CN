"""
两融账户信息数据提供者

东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息
接口: stock_margin_account_info
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockMarginAccountInfoProvider(SimpleProvider):
    """两融账户信息数据提供者"""
    
    # 必填属性
    collection_name = "stock_margin_account_info"
    display_name = "两融账户信息"
    akshare_func = "stock_margin_account_info"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-融资融券-融资融券账户统计-两融账户信息"
    collection_route = "/stocks/collections/stock_margin_account_info"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "融资余额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "融券余额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "融资买入额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "融券卖出额", "type": "float64", "description": "注意单位: 亿"},
        {"name": "证券公司数量", "type": "float64", "description": "注意单位: 家"},
        {"name": "营业部数量", "type": "float64", "description": "注意单位: 家"},
        {"name": "个人投资者数量", "type": "float64", "description": "注意单位: 万名"},
        {"name": "机构投资者数量", "type": "float64", "description": "注意单位: 家"},
        {"name": "参与交易的投资者数量", "type": "float64", "description": "注意单位: 名"},
        {"name": "有融资融券负债的投资者数量", "type": "float64", "description": "注意单位: 名"},
        {"name": "担保物总价值", "type": "float64", "description": "注意单位: 亿"},
        {"name": "平均维持担保比例", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
