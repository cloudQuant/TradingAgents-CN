"""
东方财富-成份股数据提供者

东方财富-沪深板块-概念板块-板块成份
接口: stock_board_concept_cons_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBoardConceptConsEmProvider(SimpleProvider):
    """东方财富-成份股数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_concept_cons_em"
    display_name = "东方财富-成份股"
    akshare_func = "stock_board_concept_cons_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-沪深板块-概念板块-板块成份"
    collection_route = "/stocks/collections/stock_board_concept_cons_em"
    collection_category = "板块数据"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 手"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "市盈率-动态", "type": "float64", "description": "-"},
        {"name": "市净率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
