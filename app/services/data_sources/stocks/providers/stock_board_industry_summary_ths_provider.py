"""
同花顺-同花顺行业一览表数据提供者

同花顺-同花顺行业一览表
接口: stock_board_industry_summary_ths
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBoardIndustrySummaryThsProvider(SimpleProvider):
    """同花顺-同花顺行业一览表数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_industry_summary_ths"
    display_name = "同花顺-同花顺行业一览表"
    akshare_func = "stock_board_industry_summary_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-同花顺行业一览表"
    collection_route = "/stocks/collections/stock_board_industry_summary_ths"
    collection_category = "板块数据"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "总成交量", "type": "float64", "description": "注意单位: 万手"},
        {"name": "总成交额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "净流入", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "上涨家数", "type": "float64", "description": "-"},
        {"name": "下跌家数", "type": "float64", "description": "-"},
        {"name": "均价", "type": "float64", "description": "-"},
        {"name": "领涨股", "type": "float64", "description": "-"},
        {"name": "领涨股-最新价", "type": "object", "description": "-"},
        {"name": "领涨股-涨跌幅", "type": "object", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
