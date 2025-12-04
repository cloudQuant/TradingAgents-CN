"""
千股千评数据提供者

东方财富网-数据中心-特色数据-千股千评
接口: stock_comment_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockCommentEmProvider(SimpleProvider):
    """千股千评数据提供者"""
    
    # 必填属性
    collection_name = "stock_comment_em"
    display_name = "千股千评"
    akshare_func = "stock_comment_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-千股千评"
    collection_route = "/stocks/collections/stock_comment_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "市盈率", "type": "float64", "description": "-"},
        {"name": "主力成本", "type": "float64", "description": "-"},
        {"name": "机构参与度", "type": "float64", "description": "-"},
        {"name": "综合得分", "type": "float64", "description": "-"},
        {"name": "上升", "type": "int64", "description": "注意: 正负号"},
        {"name": "目前排名", "type": "int64", "description": "-"},
        {"name": "关注指数", "type": "float64", "description": "-"},
        {"name": "交易日", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
