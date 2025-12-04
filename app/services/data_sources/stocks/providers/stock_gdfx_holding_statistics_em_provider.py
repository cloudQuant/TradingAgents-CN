"""
股东持股统计-十大股东数据提供者

东方财富网-数据中心-股东分析-股东持股统计-十大股东
接口: stock_gdfx_holding_statistics_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGdfxHoldingStatisticsEmProvider(BaseProvider):
    """股东持股统计-十大股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_gdfx_holding_statistics_em"
    display_name = "股东持股统计-十大股东"
    akshare_func = "stock_gdfx_holding_statistics_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股东分析-股东持股统计-十大股东"
    collection_route = "/stocks/collections/stock_gdfx_holding_statistics_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股东类型", "type": "object", "description": "-"},
        {"name": "统计次数", "type": "int64", "description": "-"},
        {"name": "公告日后涨幅统计-10个交易日-平均涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-10个交易日-最大涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-10个交易日-最小涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-30个交易日-平均涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-30个交易日-最大涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-30个交易日-最小涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-60个交易日-平均涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-60个交易日-最大涨幅", "type": "float64", "description": "-"},
        {"name": "公告日后涨幅统计-60个交易日-最小涨幅", "type": "float64", "description": "-"},
        {"name": "持有个股", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
