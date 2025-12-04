"""
货币数据集合元信息配置
定义所有货币数据集合的静态元信息，用于动态注册和前端展示
"""

CURRENCY_COLLECTION_METADATA = {
    # 01. 货币报价最新数据
    "currency_latest": {
        "display_name": "货币报价最新数据",
        "description": "货币报价最新数据，返回指定货币的最新报价",
        "route": "/currencies/collections/currency_latest",
        "order": 1,
    },
    # 02. 货币报价历史数据
    "currency_history": {
        "display_name": "货币报价历史数据",
        "description": "货币报价历史数据，返回指定货币在指定交易日的报价",
        "route": "/currencies/collections/currency_history",
        "order": 2,
    },
    # 03. 货币报价时间序列数据
    "currency_time_series": {
        "display_name": "货币报价时间序列数据",
        "description": "货币报价时间序列数据，返回指定货币在指定日期范围的报价",
        "route": "/currencies/collections/currency_time_series",
        "order": 3,
    },
    # 04. 货币基础信息查询
    "currency_currencies": {
        "display_name": "货币基础信息查询",
        "description": "所有货币的基础信息，包含名称、代码、符号等",
        "route": "/currencies/collections/currency_currencies",
        "order": 4,
    },
    # 05. 货币对价格转换
    "currency_convert": {
        "display_name": "货币对价格转换",
        "description": "指定货币对指定货币数量的转换后价格",
        "route": "/currencies/collections/currency_convert",
        "order": 5,
    },
}
