"""
东方财富-行业板块数据提供者

东方财富-沪深京板块-行业板块
接口: stock_board_industry_name_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBoardIndustryNameEmProvider(SimpleProvider):
    """东方财富-行业板块数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_industry_name_em"
    display_name = "东方财富-行业板块"
    akshare_func = "stock_board_industry_name_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-沪深京板块-行业板块"
    collection_route = "/stocks/collections/stock_board_industry_name_em"
    collection_category = "板块数据"

    # 字段信息
    field_info = [
        {"name": "排名", "type": "int64", "description": "-"},
        {"name": "板块代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位：%"},
        {"name": "总市值", "type": "int64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "注意单位：%"},
        {"name": "上涨家数", "type": "int64", "description": "-"},
        {"name": "下跌家数", "type": "int64", "description": "-"},
        {"name": "领涨股票", "type": "object", "description": "-"},
        {"name": "领涨股票-涨跌幅", "type": "float64", "description": "注意单位：%"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
