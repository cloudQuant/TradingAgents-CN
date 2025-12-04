"""
现金流量表数据提供者

东方财富-数据中心-年报季报-业绩快报-现金流量表
接口: stock_xjll_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockXjllEmProvider(BaseProvider):
    """现金流量表数据提供者"""
    
    # 必填属性
    collection_name = "stock_xjll_em"
    display_name = "现金流量表"
    akshare_func = "stock_xjll_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-年报季报-业绩快报-现金流量表"
    collection_route = "/stocks/collections/stock_xjll_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "净现金流-净现金流", "type": "float64", "description": "注意单位: 元"},
        {"name": "净现金流-同比增长", "type": "float64", "description": "注意单位: %"},
        {"name": "经营性现金流-现金流量净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "经营性现金流-净现金流占比", "type": "float64", "description": "注意单位: %"},
        {"name": "投资性现金流-现金流量净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "投资性现金流-净现金流占比", "type": "float64", "description": "注意单位: %"},
        {"name": "融资性现金流-现金流量净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "融资性现金流-净现金流占比", "type": "float64", "description": "注意单位: %"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
