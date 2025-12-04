"""
A 股等权重与中位数市盈率数据提供者

乐咕乐股-A 股等权重市盈率与中位数市盈率
接口: stock_a_ttm_lyr
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockATtmLyrProvider(SimpleProvider):
    """A 股等权重与中位数市盈率数据提供者"""
    
    # 必填属性
    collection_name = "stock_a_ttm_lyr"
    display_name = "A 股等权重与中位数市盈率"
    akshare_func = "stock_a_ttm_lyr"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-A 股等权重市盈率与中位数市盈率"
    collection_route = "/stocks/collections/stock_a_ttm_lyr"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "middlePETTM", "type": "float64", "description": "全A股滚动市盈率(TTM)中位数"},
        {"name": "averagePETTM", "type": "float64", "description": "全A股滚动市盈率(TTM)等权平均"},
        {"name": "middlePELYR", "type": "float64", "description": "全A股静态市盈率(LYR)中位数"},
        {"name": "averagePELYR", "type": "float64", "description": "全A股静态市盈率(LYR)等权平均"},
        {"name": "quantileInAllHistoryMiddlePeTtm", "type": "float64", "description": "当前"TTM(滚动市盈率)中位数"在历史数据上的分位数"},
        {"name": "quantileInRecent10YearsMiddlePeTtm", "type": "float64", "description": "当前"TTM(滚动市盈率)中位数"在最近10年数据上的分位数"},
        {"name": "quantileInAllHistoryAveragePeTtm", "type": "float64", "description": "当前"TTM(滚动市盈率)等权平均"在历史数据上的分位数"},
        {"name": "quantileInRecent10YearsAveragePeTtm", "type": "float64", "description": "当前"TTM(滚动市盈率)等权平均"在在最近10年数据上的分位数"},
        {"name": "quantileInAllHistoryMiddlePeLyr", "type": "float64", "description": "当前"LYR(静态市盈率)中位数"在历史数据上的分位数"},
        {"name": "quantileInRecent10YearsMiddlePeLyr", "type": "float64", "description": "当前"LYR(静态市盈率)中位数"在最近10年数据上的分位数"},
        {"name": "quantileInAllHistoryAveragePeLyr", "type": "float64", "description": "当前"LYR(静态市盈率)等权平均"在历史数据上的分位数"},
        {"name": "quantileInRecent10YearsAveragePeLyr", "type": "float64", "description": "当前"LYR(静态市盈率)等权平均"在最近10年数据上的分位数"},
        {"name": "close", "type": "float64", "description": "沪深300指数"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
