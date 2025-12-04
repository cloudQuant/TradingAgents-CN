"""
巴菲特指标数据提供者

乐估乐股-底部研究-巴菲特指标
接口: stock_buffett_index_lg
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBuffettIndexLgProvider(SimpleProvider):
    """巴菲特指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_buffett_index_lg"
    display_name = "巴菲特指标"
    akshare_func = "stock_buffett_index_lg"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐估乐股-底部研究-巴菲特指标"
    collection_route = "/stocks/collections/stock_buffett_index_lg"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "交易日"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "总市值", "type": "float64", "description": "A股收盘价*已发行股票总股本（A股+B股+H股）"},
        {"name": "GDP", "type": "float64", "description": "上年度国内生产总值（例如：2019年，则取2018年GDP）"},
        {"name": "近十年分位数", "type": "float64", "description": "当前"总市值/GDP"在历史数据上的分位数"},
        {"name": "总历史分位数", "type": "float64", "description": "当前"总市值/GDP"在历史数据上的分位数"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
