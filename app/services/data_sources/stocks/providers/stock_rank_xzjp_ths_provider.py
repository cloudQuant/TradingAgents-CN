"""
险资举牌数据提供者

同花顺-数据中心-技术选股-险资举牌
接口: stock_rank_xzjp_ths
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockRankXzjpThsProvider(SimpleProvider):
    """险资举牌数据提供者"""
    
    # 必填属性
    collection_name = "stock_rank_xzjp_ths"
    display_name = "险资举牌"
    akshare_func = "stock_rank_xzjp_ths"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-技术选股-险资举牌"
    collection_route = "/stocks/collections/stock_rank_xzjp_ths"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "举牌公告日", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "现价", "type": "float64", "description": "注意单位: 元"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "举牌方", "type": "object", "description": "-"},
        {"name": "增持数量", "type": "object", "description": "注意单位: 股"},
        {"name": "交易均价", "type": "float64", "description": "注意单位: 元"},
        {"name": "增持数量占总股本比例", "type": "float64", "description": "注意单位: %"},
        {"name": "变动后持股总数", "type": "object", "description": "注意单位: 股"},
        {"name": "变动后持股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
