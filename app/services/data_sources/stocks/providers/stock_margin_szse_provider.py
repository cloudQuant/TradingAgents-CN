"""
融资融券汇总数据提供者

深圳证券交易所-融资融券数据-融资融券汇总数据
接口: stock_margin_szse
"""
from app.services.data_sources.base_provider import BaseProvider


class StockMarginSzseProvider(BaseProvider):
    """融资融券汇总数据提供者"""
    
    # 必填属性
    collection_name = "stock_margin_szse"
    display_name = "融资融券汇总"
    akshare_func = "stock_margin_szse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深圳证券交易所-融资融券数据-融资融券汇总数据"
    collection_route = "/stocks/collections/stock_margin_szse"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "融资买入额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "融资余额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "融券卖出量", "type": "float64", "description": "注意单位: 亿股/亿份"},
        {"name": "融券余量", "type": "float64", "description": "注意单位: 亿股/亿份"},
        {"name": "融券余额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "融资融券余额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
