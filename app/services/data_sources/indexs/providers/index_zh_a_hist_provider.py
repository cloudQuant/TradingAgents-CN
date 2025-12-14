"""A股指数历史行情-通用数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class IndexZhAHistProvider(BaseProvider):
    """A股指数历史行情-通用数据提供者"""
    
    collection_name = "index_zh_a_hist"
    display_name = "A股指数历史行情-通用"
    akshare_func = "index_zh_a_hist"
    unique_keys = ["symbol", "日期"]
    
    collection_description = "东方财富网-中国股票指数行情数据（支持日/周/月）"
    collection_route = "/indexs/collections/index_zh_a_hist"
    collection_order = 5
    
    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "period": "period",
        "start_date": "start_date",
        "end_date": "end_date",
    }
    
    # 必填参数
    required_params = ["symbol"]
    
    # 添加参数到数据列
    add_param_columns = {
        "symbol": "symbol",
    }
    
    field_info = [
        {"name": "symbol", "type": "string", "description": "指数代码（如000016）"},
        {"name": "日期", "type": "string", "description": "交易日"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "成交量", "type": "int", "description": "注意单位: 手"},
        {"name": "成交额", "type": "float", "description": "注意单位: 元"},
        {"name": "振幅", "type": "float", "description": "注意单位: %"},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float", "description": "注意单位: 元"},
        {"name": "换手率", "type": "float", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
