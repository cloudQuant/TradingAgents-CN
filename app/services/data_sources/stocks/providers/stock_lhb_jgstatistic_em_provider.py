"""
机构席位追踪数据提供者

东方财富网-数据中心-龙虎榜单-机构席位追踪
接口: stock_lhb_jgstatistic_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbJgstatisticEmProvider(BaseProvider):
    """机构席位追踪数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_jgstatistic_em"
    display_name = "机构席位追踪"
    akshare_func = "stock_lhb_jgstatistic_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-机构席位追踪"
    collection_route = "/stocks/collections/stock_lhb_jgstatistic_em"
    collection_category = "龙虎榜"

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "龙虎榜成交金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "上榜次数", "type": "int64", "description": "-"},
        {"name": "机构买入额", "type": "float64", "description": "注意单位: 元"},
        {"name": "机构买入次数", "type": "int64", "description": "-"},
        {"name": "机构卖出额", "type": "float64", "description": "注意单位: 元"},
        {"name": "机构卖出次数", "type": "int64", "description": "-"},
        {"name": "机构净买额", "type": "float64", "description": "注意单位: 元"},
        {"name": "近1个月涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "近3个月涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "近6个月涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "近1年涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
