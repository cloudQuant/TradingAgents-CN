"""
沪深港通-港股通(沪>港)实时行情数据提供者

东方财富网-行情中心-沪深港通-港股通(沪>港)-股票；按股票代码排序
接口: stock_hsgt_sh_hk_spot_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHsgtShHkSpotEmProvider(SimpleProvider):
    """沪深港通-港股通(沪>港)实时行情数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_sh_hk_spot_em"
    display_name = "沪深港通-港股通(沪>港)实时行情"
    akshare_func = "stock_hsgt_sh_hk_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-沪深港通-港股通(沪>港)-股票；按股票代码排序"
    collection_route = "/stocks/collections/stock_hsgt_sh_hk_spot_em"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: HKD"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 亿股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 亿港元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
