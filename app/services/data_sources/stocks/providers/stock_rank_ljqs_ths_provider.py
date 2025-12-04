"""
量价齐升数据提供者

同花顺-数据中心-技术选股-量价齐升
接口: stock_rank_ljqs_ths
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockRankLjqsThsProvider(SimpleProvider):
    """量价齐升数据提供者"""
    
    # 必填属性
    collection_name = "stock_rank_ljqs_ths"
    display_name = "量价齐升"
    akshare_func = "stock_rank_ljqs_ths"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-技术选股-量价齐升"
    collection_route = "/stocks/collections/stock_rank_ljqs_ths"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 元"},
        {"name": "量价齐升天数", "type": "int64", "description": "-"},
        {"name": "阶段涨幅", "type": "float64", "description": "注意单位: %"},
        {"name": "累计换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
