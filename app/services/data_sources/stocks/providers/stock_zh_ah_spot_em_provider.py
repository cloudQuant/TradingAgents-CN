"""
实时行情数据-东财数据提供者

东方财富网-行情中心-沪深港通-AH股比价-实时行情, 延迟 15 分钟更新
接口: stock_zh_ah_spot_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhAhSpotEmProvider(SimpleProvider):
    """实时行情数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_ah_spot_em"
    display_name = "实时行情数据-东财"
    akshare_func = "stock_zh_ah_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-沪深港通-AH股比价-实时行情, 延迟 15 分钟更新"
    collection_route = "/stocks/collections/stock_zh_ah_spot_em"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "H股代码", "type": "object", "description": "-"},
        {"name": "最新价-HKD", "type": "float64", "description": "注意单位: HKD"},
        {"name": "H股-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "A股代码", "type": "object", "description": "-"},
        {"name": "最新价-RMB", "type": "float64", "description": "注意单位: RMB"},
        {"name": "A股-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "比价", "type": "float64", "description": "-"},
        {"name": "溢价", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
