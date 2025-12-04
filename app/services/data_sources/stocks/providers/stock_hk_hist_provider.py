"""
历史行情数据-东财数据提供者

港股-历史行情数据, 可以选择返回复权后数据, 更新频率为日频
接口: stock_hk_hist
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkHistProvider(BaseProvider):
    """历史行情数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_hist"
    display_name = "历史行情数据-东财"
    akshare_func = "stock_hk_hist"
    unique_keys = ['日期']
    
    # 可选属性
    collection_description = "港股-历史行情数据, 可以选择返回复权后数据, 更新频率为日频"
    collection_route = "/stocks/collections/stock_hk_hist"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "period": "period",
        "start_date": "start_date",
        "end_date": "end_date",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol', 'period', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "注意单位: 港元"},
        {"name": "收盘", "type": "float64", "description": "注意单位: 港元"},
        {"name": "最高", "type": "float64", "description": "注意单位: 港元"},
        {"name": "最低", "type": "float64", "description": "注意单位: 港元"},
        {"name": "成交量", "type": "int64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "注意单位: 港元"},
        {"name": "收盘", "type": "float64", "description": "注意单位: 港元"},
        {"name": "最高", "type": "float64", "description": "注意单位: 港元"},
        {"name": "最低", "type": "float64", "description": "注意单位: 港元"},
        {"name": "成交量", "type": "int64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "注意单位: 港元"},
        {"name": "收盘", "type": "float64", "description": "注意单位: 港元"},
        {"name": "最高", "type": "float64", "description": "注意单位: 港元"},
        {"name": "最低", "type": "float64", "description": "注意单位: 港元"},
        {"name": "成交量", "type": "int32", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
