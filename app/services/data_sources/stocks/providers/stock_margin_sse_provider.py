"""
融资融券汇总数据提供者

上海证券交易所-融资融券数据-融资融券汇总数据
接口: stock_margin_sse
"""
from app.services.data_sources.base_provider import BaseProvider


class StockMarginSseProvider(BaseProvider):
    """融资融券汇总数据提供者"""
    
    # 必填属性
    collection_name = "stock_margin_sse"
    display_name = "融资融券汇总"
    akshare_func = "stock_margin_sse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "上海证券交易所-融资融券数据-融资融券汇总数据"
    collection_route = "/stocks/collections/stock_margin_sse"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "信用交易日期", "type": "object", "description": "-"},
        {"name": "融资余额", "type": "int64", "description": "注意单位: 元"},
        {"name": "融资买入额", "type": "int64", "description": "注意单位: 元"},
        {"name": "融券余量", "type": "int64", "description": "-"},
        {"name": "融券余量金额", "type": "int64", "description": "注意单位: 元"},
        {"name": "融券卖出量", "type": "int64", "description": "-"},
        {"name": "融资融券余额", "type": "int64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
