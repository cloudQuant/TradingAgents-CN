"""
股东户数详情数据提供者

东方财富网-数据中心-特色数据-股东户数详情
接口: stock_zh_a_gdhs_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAGdhsDetailEmProvider(BaseProvider):
    """股东户数详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_gdhs_detail_em"
    display_name = "股东户数详情"
    akshare_func = "stock_zh_a_gdhs_detail_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股东户数详情"
    collection_route = "/stocks/collections/stock_zh_a_gdhs_detail_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "股东户数统计截止日", "type": "object", "description": "-"},
        {"name": "区间涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "股东户数-本次", "type": "int64", "description": "-"},
        {"name": "股东户数-上次", "type": "int64", "description": "-"},
        {"name": "股东户数-增减", "type": "int64", "description": "-"},
        {"name": "股东户数-增减比例", "type": "float64", "description": "注意单位: %"},
        {"name": "户均持股市值", "type": "float64", "description": "-"},
        {"name": "户均持股数量", "type": "float64", "description": "-"},
        {"name": "总市值", "type": "float64", "description": "-"},
        {"name": "总股本", "type": "int64", "description": "-"},
        {"name": "股本变动", "type": "int64", "description": "-"},
        {"name": "股本变动原因", "type": "object", "description": "-"},
        {"name": "股东户数公告日期", "type": "object", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
