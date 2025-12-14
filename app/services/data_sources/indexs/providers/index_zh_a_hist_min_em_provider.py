"""A股指数分时行情-东财数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class IndexZhAHistMinEmProvider(BaseProvider):
    """A股指数分时行情-东财数据提供者"""
    
    collection_name = "index_zh_a_hist_min_em"
    display_name = "A股指数分时行情-东财"
    akshare_func = "index_zh_a_hist_min_em"
    unique_keys = ["symbol", "时间"]
    
    collection_description = "东方财富网-指数分时行情数据（1/5/15/30/60分钟）"
    collection_route = "/indexs/collections/index_zh_a_hist_min_em"
    collection_order = 6
    
    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "period": "period",
        "start_date": "start_date",
        "end_date": "end_date",
    }
    
    # 必填参数
    required_params = ["symbol", "period"]
    
    # 添加参数到数据列
    add_param_columns = {
        "symbol": "symbol",
    }
    
    field_info = [
        {"name": "symbol", "type": "string", "description": "指数代码（如000001）"},
        {"name": "时间", "type": "string", "description": "交易时间"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "成交量", "type": "int", "description": "注意单位: 手"},
        {"name": "成交额", "type": "float", "description": "注意单位: 元"},
        {"name": "均价", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
